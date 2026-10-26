import streamlit as st
import plotly.graph_objects as go

# Page Configuration
st.set_page_config(page_title="Experiment Timeline Calculator", layout="centered")
st.title("🔬 Experiment Duration Calculator")
st.write("Adjust the parameters below to see how they impact total experiment time.")

# Sidebar Controls for User Input
st.sidebar.header("Experimental Parameters")
muscles_num = st.sidebar.slider("Number of Muscles to Test", min_value=1, max_value=4, value=4, step=1)
stim_levels = st.sidebar.slider("Number of Stimulation Intensities to Test", min_value=2, max_value=5, value=3, step=1)
positions = st.sidebar.slider("Number of Isometric Joint Positions", min_value=1, max_value=3, value=3, step=1)
velocities = st.sidebar.slider("Number of Isokinetic Joint Velocities", min_value=0, max_value=3, value=2, step=1)

reps = st.sidebar.slider("Repetitions / Williams Sequences (per condition)", min_value=1, max_value=3, value=2, step=1)
trial_duration = st.sidebar.slider("Trial (Stimulation Delivery) Duration (seconds)", min_value=1, max_value=10, value=3, step=1)
rest_between_trials = st.sidebar.slider("Rest Between Trials (seconds) [Inter-Rep]", min_value=20, max_value=60, value=30, step=5)
rest_between_blocks = st.sidebar.slider("Rest Between Major Blocks / Conditions (minutes)", min_value=1, max_value=5, value=2, step=1)

calibration_time = st.sidebar.slider("Calibration Time (per muscle, minutes)", min_value=0, max_value=45, value=15, step=5)
total_calibration_time = calibration_time * muscles_num

# Conditional Slider for Number of Sessions
if muscles_num > 1:
    number_of_sessions = st.sidebar.slider("Number of test sessions", min_value=1, max_value=3, value=2, step=1)
else:
    number_of_sessions = 1
    st.sidebar.info("Number of test sessions fixed to 1 because only 1 muscle is selected.")

# Timeline Calculations
active_velocities = velocities if velocities > 0 else 0
total_condition_states = positions + active_velocities

# Total trials: Muscles x Joint States x Williams Stim Levels x Reps
total_trials = muscles_num * total_condition_states * stim_levels * reps
total_trials_persesh = total_trials / number_of_sessions

# Total trial active time (seconds)
total_active_seconds = total_trials * trial_duration

# Total major blocks (Each rep acts as a complete Williams sequence block per joint state)
total_block_count = muscles_num * total_condition_states * reps
total_block_count_persesh  = total_block_count/ number_of_sessions;

# Inter-trial rest occurs between individual stimulations within the sequences
total_rep_breaks_all = total_trials - total_block_count
total_trial_rest_seconds = total_rep_breaks_all * rest_between_trials

# Total major block/condition transitions requiring longer rest (minutes)
total_major_block_transitions = total_block_count - 1 if total_block_count > 1 else 0
total_block_rest_minutes = total_major_block_transitions * rest_between_blocks

# Convert everything to minutes (Total across entire study)
active_mins = total_active_seconds / 60
trial_rest_mins = total_trial_rest_seconds / 60
block_rest_mins = total_block_rest_minutes

total_experiment_time = total_calibration_time + active_mins + trial_rest_mins + block_rest_mins
total_experiment_time_persesh = total_experiment_time / number_of_sessions

# --- Display Metrics Above Chart ---
st.subheader("⏱️ Estimated Time & Stimulations")
col1, col2 = st.columns(2)
with col1:
    st.metric(label="Duration Per Session", value=f"{total_experiment_time_persesh:.1f} mins")
with col2:
    st.metric(label="Total Study Duration", value=f"{total_experiment_time:.1f} mins")

st.metric(label="Total Number of Stimulations Administered Per Session", value=f"{total_trials_persesh:.0f}") 

# Block Breakdown Explanations
st.subheader("📋 Experimental Block Hierarchy")
st.markdown(f"""
* **Joint/Condition Blocks:** **{total_condition_states}** total joint configurations ({positions} isometric positions + {active_velocities} active isokinetic velocities).
* **Williams Design Sequences:** **{stim_levels}** stimulation intensities randomized per sequence, repeated for **{reps}** complete block sets.
* **Total Major Blocks in a Session:** **{total_block_count_persesh}** (product of: number of muscles, joint state configurations, and repetitions) total major blocks across the study, requiring **{total_major_block_transitions}** inter-block rest breaks of {rest_between_blocks} minutes each.
""")

# --- Per-Session Data for the Interactive Breakdown Chart ---
labels = ['Calibration Time', 'Active Trial Time', 'Rep Rest (Intra-Block)', 'Block Rest (Inter-Block)']
# Divide by number_of_sessions so the pie chart accurately reflects per-session time blocks
values = [
    total_calibration_time / number_of_sessions, 
    active_mins / number_of_sessions, 
    trial_rest_mins / number_of_sessions, 
    block_rest_mins / number_of_sessions
]

# Filter out zero values to keep the chart clean
filtered_labels = [l for l, v in zip(labels, values) if v > 0]
filtered_values = [v for v in values if v > 0]

# Build Plotly Chart
fig = go.Figure(data=[go.Pie(
    labels=filtered_labels,
    values=filtered_values,
    hole=.4,
    textinfo='value+percent',
    hovertemplate="%{label}: %{value:.1f} mins<extra></extra>"
)])

fig.update_layout(
    title_text="Per-Session Time Allocation Breakdown (Minutes)",
    annotations=[dict(text='Mins', x=0.5, y=0.5, font_size=20, showarrow=False)],
    showlegend=True
)

st.plotly_chart(fig, use_container_width=True)

# Explanation Note Under Pie Chart
st.markdown("---")
st.markdown(
    "💡 **Note on Calibration Time:** This represents the time required to establish "
    "the participant's simulation levels that elicit the target levels of torque."
)
