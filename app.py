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
velocities = st.sidebar.slider("Number of Isokinetic Joint Velocities", min_value=0, max_value=2, value=2, step=1)

reps = st.sidebar.slider("Repetitions (per stimulation intensity)", min_value=1, max_value=3, value=2, step=1)
trial_duration = st.sidebar.slider("Trial Duration (seconds)", min_value=1, max_value=10, value=5, step=2)
rest_between_trials = st.sidebar.slider("Rest Between Trials (seconds)", min_value=20, max_value=60, value=30, step=5)
rest_between_stim_level = st.sidebar.slider("Rest Between blocks (minutes)", min_value=0, max_value=5, value=2, step=1)
setup_time = st.sidebar.slider("Level Tuning & Prep Time (minutes)", min_value=0, max_value=45, value=30, step=5)

# Conditional Slider for Number of Sessions
if muscles_num > 1:
    number_of_sessions = st.sidebar.slider("Number of test sessions", min_value=1, max_value=2, value=2, step=1)
else:
    number_of_sessions = 1
    st.sidebar.info("Number of test sessions fixed to 1 because only 1 muscle is selected.")


# Timeline Calculations
total_trials = muscles_num * stim_levels * reps * ( positions + velocities)
total_trials_persesh = total_trials/number_of_sessions;

# Total trial active time (seconds)
total_active_seconds = total_trials * trial_duration

# Total rest between trials (seconds)
# Within a condition, rest occurs between reps. Total breaks = stim_levels * (reps - 1)
total_trial_breaks = stim_levels * (reps - 1) if reps > 1 else 0
total_trial_rest_seconds = total_trial_breaks * rest_between_trials

# Total rest between stim_levels (minutes)
total_condition_breaks = stim_levels - 1 if stim_levels > 1 else 0
#total_condition_rest_minutes = total_condition_breaks * rest_between_stim_levels

# Convert everything to minutes
active_mins = total_active_seconds / 60
trial_rest_mins = total_trial_rest_seconds / 60
#condition_rest_mins = total_condition_rest_minutes
#total_experiment_time = setup_time + active_mins + trial_rest_mins + condition_rest_mins
total_experiment_time = setup_time + active_mins + trial_rest_mins 


# Display Metrics
st.subheader("⏱️ Total Estimated Time")
st.metric(label="Total Duration", value=f"{total_experiment_time:.1f} minutes")
st.metric(label="Total Number of Stimulations Administered Per Session", value = f"{total_trials_persesh:.0f}") 

# Data for the interactive breakdown chart
labels = ['Prep Time', 'Active Trial Time', 'Rest Between Trials']
#values = [setup_time, active_mins, trial_rest_mins, condition_rest_mins]
values = [setup_time, active_mins, trial_rest_mins]


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
    title_text="Time Allocation Breakdown (Minutes)",
    annotations=[dict(text='Mins', x=0.5, y=0.5, font_size=20, showarrow=False)],
    showlegend=True
)

st.plotly_chart(fig, use_container_width=True)
