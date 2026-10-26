import streamlit as st
import plotly.graph_objects as go

# Page Configuration
st.set_page_config(page_title="Experiment Timeline Calculator", layout="centered")
st.title("🔬 Experiment Duration Calculator")
st.write("Adjust the parameters below to see how they impact total experiment time.")

# Sidebar Controls for User Input
st.sidebar.header("Experimental Parameters")
conditions = st.sidebar.slider("Number of Conditions", min_value=2, max_value=5, value=3, step=1)
reps = st.sidebar.slider("Repetitions (per condition)", min_value=1, max_value=3, value=2, step=1)
trial_duration = st.sidebar.slider("Trial Duration (seconds)", min_value=1, max_value=10, value=5, step=2)
rest_between_trials = st.sidebar.slider("Rest Between Trials (seconds)", min_value=30, max_value=60, value=30, step=5)
rest_between_conditions = st.sidebar.slider("Rest Between blocks (minutes)", min_value=0, max_value=5, value=2, step=1)
setup_time = st.sidebar.slider("Initial Setup/Prep Time (minutes)", min_value=0, max_value=60, value=15, step=5)

# Timeline Calculations
total_trials = conditions * reps

# Total trial active time (seconds)
total_active_seconds = total_trials * trial_duration

# Total rest between trials (seconds)
# Within a condition, rest occurs between reps. Total breaks = conditions * (reps - 1)
total_trial_breaks = conditions * (reps - 1) if reps > 1 else 0
total_trial_rest_seconds = total_trial_breaks * rest_between_trials

# Total rest between conditions (minutes)
total_condition_breaks = conditions - 1 if conditions > 1 else 0
total_condition_rest_minutes = total_condition_breaks * rest_between_conditions

# Convert everything to minutes
active_mins = total_active_seconds / 60
trial_rest_mins = total_trial_rest_seconds / 60
condition_rest_mins = total_condition_rest_minutes
total_experiment_time = setup_time + active_mins + trial_rest_mins + condition_rest_mins

# Display Metrics
st.subheader("⏱️ Total Estimated Time")
st.metric(label="Total Duration", value=f"{total_experiment_time:.1f} minutes")
st.metric(label="Number of Stimulations", value = f"{total_trials:.0f}") 

# Data for the interactive breakdown chart
labels = ['Initial Setup', 'Active Trial Time', 'Rest Between Trials', 'Rest Between Conditions']
values = [setup_time, active_mins, trial_rest_mins, condition_rest_mins]

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
