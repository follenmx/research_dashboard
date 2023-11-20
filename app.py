import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import plotly.express as px

#Page Setup
st.set_page_config(page_title='CFRM Research 2023',
                   page_icon="🧊",
                   layout='wide',
                   initial_sidebar_state="expanded")

data_link = st.secrets['data_link']

#Data fetch
@st.cache_data
def load_data():
    df = pd.read_csv(data_link, sep=';')    
    return df
df = load_data()

# Display number of submissions
st.sidebar.markdown(f"**Total Submissions: {len(df)}**")

st.title("CFRM Research: Data Analysis")
st.sidebar.subheader("Please filter the data:")

#FILTERS
gender_filter = st.sidebar.multiselect(
    "Please select Gender",
    options=df['Gender of the person interviewed'].unique(),
    default=df['Gender of the person interviewed'].unique()
)
usage_filter = st.sidebar.multiselect(
    "Please select type of usage of CFRM",
    options=df["How often have you interacted INTERSOS' Complaint, Feedback, and Response Mechanism (CFRM)?"].unique(),
    default=df["How often have you interacted INTERSOS' Complaint, Feedback, and Response Mechanism (CFRM)?"].unique()
)

district_filter = st.sidebar.multiselect(
    "Please select district",
    options=df['District'].unique(),
    default=df['District'].unique()
)

#Filter query
df_query = "`Gender of the person interviewed` == @gender_filter & `How often have you interacted INTERSOS' Complaint, Feedback, and Response Mechanism (CFRM)?` == @usage_filter& `District` ==  @district_filter"
df = df.query(df_query)


# Charts Section
st.subheader('Gender & Age Disaggregation')
# -- Pie Chart - Gender

# Calculate the counts for each age group
gender_counts = df['Gender of the person interviewed'].value_counts()

# Create the pie chart with a blue color scheme
fig_gender = px.pie(
    gender_counts,
    values=gender_counts.values,
    names=gender_counts.index,
    title='Gender Disaggregation',
    color_discrete_sequence=px.colors.sequential.RdBu_r  # Set the color scheme to blue
)

# Customize layout for clarity and visibility
fig_gender.update_traces(
    textinfo='percent+label',
    marker=dict(line=dict(color='#000000', width=2))  # Adds a line around each segment
)

# Set transparent background
fig_gender.update_layout(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    showlegend=True
)
st.plotly_chart(fig_gender, use_container_width=True)

# --- end of pie chart gender

# -- Pie Chart - Age

conditions = [
    (df['Age of the person interviewed'] <= 17),
    ((df['Age of the person interviewed'] > 17) & (df['Age of the person interviewed'] <= 59)),
    (df['Age of the person interviewed'] > 59)
]

labels = ['0-17 years', '18-59 years', '59+ years']

df['AgeGroup'] = np.select(conditions, labels, default='Unknown')


# Calculate the counts for each age group
age_group_counts = df['AgeGroup'].value_counts()

# Create the pie chart with a blue color scheme
fig_age = px.pie(
    age_group_counts,
    values=age_group_counts.values,
    names=age_group_counts.index,
    title='Age Disaggregation',
    color_discrete_sequence=px.colors.sequential.RdBu_r  # Set the color scheme to blue
)

# Customize layout for clarity and visibility
fig_age.update_traces(
    textinfo='percent+label',
    marker=dict(line=dict(color='#000000', width=2))  # Adds a line around each segment
)

# Set transparent background
fig_age.update_layout(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    showlegend=True
)

st.plotly_chart(fig_age, use_container_width=True)

# --- end age pie chart
st.markdown('---')

# -- Bar Chart - Impairments

potential_answers = [
    "Difficulty seeing, even if wearing glasses",
    "Difficulty hearing, even if using a hearing aid",
    "Difficulty walking or climbing steps",
    "Difficulty remembering or concentrating",
    "None of the above"
]
pwd = df['If you encounter any difficulties from this list, please select which']
pwd_counts = {answer: pwd.str.count(answer).sum() for answer in potential_answers}

df_pwd = pd.DataFrame(list(pwd_counts.items()), columns=['Answer', 'Count'])

# Sort data for better visualization
df_pwd_sorted = df_pwd.sort_values('Count', ascending=False)


# Create the bar chart with simplified x-axis
fig_pwd = px.bar(
    df_pwd_sorted,
    x='Answer',
    y='Count',
    text_auto=True,  # Automatically add text on bars
    title='Type of Impairments',
    color='Answer',  # Color by answer
    color_continuous_scale='blues'  # Use a blue color scale
)

# Customize the chart layout
fig_pwd.update_layout(
    xaxis_title="",
    yaxis_title="Count",
    plot_bgcolor='rgba(0,0,0,0)',  # Transparent background
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(color='white'),  # Adjust font color for readability
    showlegend=True  # Ensure the legend is shown
)

# Customize x-axis to remove the labels
fig_pwd.update_xaxes(showticklabels=False)  # Hide x-axis labels

# Customize bar appearance
fig_pwd.update_traces(
    marker_line_color='rgb(8,48,107)',  # Dark blue border for bars
    marker_line_width=1.5,  # Width of the border
    opacity=0.8  # Adjust for slight transparency
)
st.plotly_chart(fig_pwd, use_container_width=True)

# --- end bar chart impairments

st.markdown('---')

# -- Pie Chart Usage of CFRM

usage_counts = df["How often have you interacted INTERSOS' Complaint, Feedback, and Response Mechanism (CFRM)?"].value_counts()

# Create the pie chart
fig_usage = px.pie(
    usage_counts,
    values=usage_counts.values,
    names=usage_counts.index,
    title='CFRM Usage (How often you used CFRM?)',
    color_discrete_sequence=px.colors.sequential.RdBu_r  # Optional: for a nice color sequence
)

# Customize layout for clarity and visibility
fig_usage.update_traces(
    textinfo='percent+label',
    marker=dict(line=dict(color='#000000', width=2)),  # Optional: adds a line around each segment
    pull=[0.1 if usage_counts[i] == usage_counts.max() else 0 for i in range(len(usage_counts))]  # Optional: pulls the largest segment slightly out
)

# Set transparent background
fig_usage.update_layout(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    showlegend=True
)

# Show the fig_usageure
st.plotly_chart(fig_usage, use_container_width=True)

# --- end of the chart 

st.markdown('---')
st.subheader('Insights on CFRM Awareness')
# -- Pie Chart Informed Status

# Replace long sentences with shorter labels
df["Are you informed about INTERSOS' Complaint, Feedback, and Response Mechanism (CFRM)?"].replace({
    'Yes, I am informed about the CFRM.': 'Informed',
    "I heard about it but don't know the details.": 'Partially Informed',
    'No, I am not aware of the CFRM.': 'Not aware'
}, inplace=True)

# Calculate the counts for CFRM awareness
cfrm_awareness_counts = df["Are you informed about INTERSOS' Complaint, Feedback, and Response Mechanism (CFRM)?"].value_counts()

# Create the pie chart with an appropriate color scheme
fig_cfrm_awareness = px.pie(
    cfrm_awareness_counts,
    values=cfrm_awareness_counts.values,
    names=cfrm_awareness_counts.index,
    title='CFRM Awareness Disaggregation',
    color_discrete_sequence=px.colors.sequential.RdBu_r  # Reversed Red-Blue color scheme
)

# Customize layout for clarity and visibility
fig_cfrm_awareness.update_traces(
    textinfo='percent+label',
    marker=dict(line=dict(color='#000000', width=2))  # Adds a line around each segment
)

# Set transparent background
fig_cfrm_awareness.update_layout(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    showlegend=True
)

st.plotly_chart(fig_cfrm_awareness, use_container_width=True)

#--- chart ends

# -- Bar Chart Info

potential_answers = [
    "Poster/Leaflet;",
    "Capacity Building Activities;",
    "Social Media;",
    "Directly from INTERSOS staff;",
    "Word of mouth;",
    "Other;"
]
info_sharing = df["How did you learn about INTERSOS' Complaint, Feedback, and Response Mechanism (CFRM)?"]
info_sharing_counts = {answer: info_sharing.str.count(answer).sum() for answer in potential_answers}

df_info_sharing = pd.DataFrame(list(info_sharing_counts.items()), columns=['Answer', 'Count'])

# Sort data for better visualization
df_info_sharing_sorted = df_info_sharing.sort_values('Count', ascending=False)

# Create the bar chart with a consistent color scheme
fig_info = px.bar(
    df_info_sharing_sorted,
    x='Answer',
    y='Count',
    text_auto=True,  # Automatically add text on bars
    title='Ways People Learned About CFRM',
    color='Answer',  # Color by answer
    color_discrete_sequence=px.colors.sequential.RdBu_r  # Use a blue color scale consistent with other charts
)

# Customize the chart layout
fig_info.update_layout(
    xaxis_title="Information Source",
    yaxis_title="Count",
    plot_bgcolor='rgba(0,0,0,0)',  # Transparent background
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(color='white'),  # Adjust font color for readability
    showlegend=False  # Hide the legend if not necessary
)

# Customize bar appearance
fig_info.update_traces(
    marker_line_color='rgb(8,48,107)',  # Dark blue border for bars
    marker_line_width=1.5,  # Width of the border
    opacity=0.8,
    textangle=0  # Set text angle to 0 for horizontal alignment  # Adjust for slight transparency
)

st.plotly_chart(fig_info, use_container_width=True)

# --- chart ends 

# -- Bar Chart Prefered Info Sharin 

potential_answers = [
    "Poster/Leaflet;",
    "Capacity Building Activities;",
    "Social Media;",
    "Directly from INTERSOS staff;",
    "Word of mouth;",
    "Email",
    "Phone",
    "Other;"
]
info_sharing = df["How would you prefer to receive information about INTERSOS' Complaint, Feedback, and Response Mechanism (CFRM)?"]
info_sharing_counts = {answer: info_sharing.str.count(answer).sum() for answer in potential_answers}

df_info_sharing = pd.DataFrame(list(info_sharing_counts.items()), columns=['Answer', 'Count'])
df_info_sharing_sorted = df_info_sharing.sort_values('Count', ascending=False)

# Create the bar chart with a consistent color scheme
fig_preferred_info = px.bar(
    df_info_sharing_sorted,
    x='Answer',
    y='Count',
    text_auto=True,  # Automatically add text on bars
    title='Preferred Ways to Learn About CFRM',
    color='Answer',  # Color by answer
    color_discrete_sequence=px.colors.sequential.RdBu_r  # Use a blue color scale consistent with other charts
)

# Customize the chart layout
fig_preferred_info.update_layout(
    xaxis_title="Preferred Information Source",
    yaxis_title="Count",
    plot_bgcolor='rgba(0,0,0,0)',  # Transparent background
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(color='white'),  # Adjust font color for readability
    showlegend=False  # Hide the legend if not necessary
)

# Customize bar appearance
fig_preferred_info.update_traces(
    marker_line_color='rgb(8,48,107)',  # Dark blue border for bars
    marker_line_width=1.5,  # Width of the border
    opacity=0.8,
    textangle = 0  # Adjust for slight transparency
)

st.plotly_chart(fig_preferred_info, use_container_width=True)
# --- ends chart

st.markdown('---')

# -- Bar Chart complaint choice

df['Would you try to solve your problem on your own before submitting a complaint?'].replace({
    'Yes, definitely': 'Definitely',
    "I'd consider it": 'Consider',
    'Possibly, depending on the issue': 'Possibly',
    'Unlikely, but not ruled out': 'Unlikely',
    "No, I'd go straight to a complaint": 'Straight to Complaint'
}, inplace=True)

response_counts = df['Would you try to solve your problem on your own before submitting a complaint?'].value_counts()

# Assuming response_counts is a Series with the count of each response
categories = ['Straight to Complaint', 'Unlikely', 'Possibly', 'Consider', 'Definitely']
counts = [response_counts.get(category, 0) for category in categories]

# Define a gradient color scale from bright blue to red
color_scale = ['blue', 'lightblue', 'lightcoral', 'coral', 'red']

# Create the diverging bar chart
fig_complaint_choice = go.Figure()

# Adding bars for each response category
for i, category in enumerate(categories):
    fig_complaint_choice.add_trace(go.Bar(
        x=[category],
        y=[counts[i]],
        name=category,
        marker_color=color_scale[i],
        marker_line_color='rgb(8,48,107)',
        marker_line_width=1.5,
        opacity=0.8
    ))

# Customize the layout
fig_complaint_choice.update_layout(
    title='Q: Would you try to solve your problem on your own before submitting a complaint?',
    xaxis=dict(title='Response Categories'),
    yaxis=dict(title='Count of Responses'),
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(color='white'),
    barmode='relative',
    showlegend=False
)

st.plotly_chart(fig_complaint_choice, use_container_width= True)

# --- end of the chart
st.markdown('---')
st.subheader('Likelihood of complaint submision')

# Calculate the counts for each age group
non_sensitive_comp = df['How likely are you to submit a non-sensitive complaint?'].value_counts()

# Create the bar chart with a consistent color scheme
fig_nonsens = px.bar(
    non_sensitive_comp,
    x=non_sensitive_comp.index,
    y=non_sensitive_comp.values,
    text_auto=True,  # Automatically add text on bars
    title='How Likely Are You to Submit a Non-Sensitive Complaint?',
    color = non_sensitive_comp.index,
    color_discrete_sequence=px.colors.sequential.RdBu_r  # Use a blue color scale consistent with other charts
)

# Customize the chart layout
fig_nonsens.update_layout(
    xaxis_title="Response",
    yaxis_title="Count",
    plot_bgcolor='rgba(0,0,0,0)',  # Transparent background
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(color='white'),  # Adjust font color for readability
    showlegend=False  # Hide the legend if not necessary
)

# Customize bar appearance
fig_nonsens.update_traces(
    marker_line_color='rgb(8,48,107)',  # Dark blue border for bars
    marker_line_width=1.5,  # Width of the border
    opacity=0.8  # Adjust for slight transparency
)

# Show the figure
st.plotly_chart(fig_nonsens, use_container_width=True)

# --- chart ends 

# -- Bar Chart sens comp

# Calculate the counts for each age group
non_sensitive_comp = df['How likely are you to submit a sensitive complaint?'].value_counts()

# Create the bar chart with a consistent color scheme
fig_sens_comp = px.bar(
    non_sensitive_comp,
    x=non_sensitive_comp.index,
    y=non_sensitive_comp.values,
    text_auto=True,  # Automatically add text on bars
    title='How Likely Are You to Submit a Sensitive Complaint?',
    color = non_sensitive_comp.index,
    color_discrete_sequence=px.colors.sequential.RdBu_r  # Use a blue color scale consistent with other charts
)

# Customize the chart layout
fig_sens_comp.update_layout(
    xaxis_title="Response",
    yaxis_title="Count",
    plot_bgcolor='rgba(0,0,0,0)',  # Transparent background
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(color='white'),  # Adjust font color for readability
    showlegend=False  # Hide the legend if not necessary
)

# Customize bar appearance
fig_sens_comp.update_traces(
    marker_line_color='rgb(8,48,107)',  # Dark blue border for bars
    marker_line_width=1.5,  # Width of the border
    opacity=0.8  # Adjust for slight transparency
)

st.plotly_chart(fig_sens_comp, use_container_width=True)

# -- Bar Chart Concerns 

potential_answers = [
    "Transparency;",
    "Timeliness of responses;",
    "Lack of accessibility;",
    "Data security;",
    "Language barriers;"
]

concerns_cfrm = df["What concerns do you have about INTERSOS' Complaint, Feedback and Response Mechanisms(CFRM)?"]
conncerns_counts = {answer: concerns_cfrm.str.count(answer).sum() for answer in potential_answers}

df_concerns = pd.DataFrame(list(conncerns_counts.items()), columns=['Answer', 'Count'])
df_concerns_sorted = df_concerns.sort_values('Count', ascending=False)

# Create the bar chart with a consistent color scheme
fig_concerns = px.bar(
    df_concerns_sorted,
    x='Answer',
    y='Count',
    text_auto=True,  # Automatically add text on bars
    title='Preferred Ways to Learn About CFRM',
    color='Answer',  # Color by answer
    color_discrete_sequence=px.colors.sequential.RdBu_r  # Use a blue color scale consistent with other charts
)

# Customize the chart layout
fig_concerns.update_layout(
    xaxis_title="Beneficiary Concerns about CFRM",
    yaxis_title="Count",
    plot_bgcolor='rgba(0,0,0,0)',  # Transparent background
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(color='white'),  # Adjust font color for readability
    showlegend=False  # Hide the legend if not necessary
)

# Customize bar appearance
fig_concerns.update_traces(
    marker_line_color='rgb(8,48,107)',  # Dark blue border for bars
    marker_line_width=1.5,  # Width of the border
    opacity=0.8  # Adjust for slight transparency
)

st.plotly_chart(fig_concerns, use_container_width=True)

# --- end 
st.markdown('---')

# -- Bar Chart Submiting Option 

submit_option = df["How did you submit your complaint/feedback?"].value_counts()

fig_so = px.bar(submit_option, 
                x=submit_option.index,
                y=submit_option.values,
                text_auto=True,  # Automatically add text on bars
                title='How did you submit your complaint/feedback?',
                color = submit_option.index,
                 color_discrete_sequence=px.colors.sequential.RdBu_r  # Use a blue color scale consistent with other charts
                 )
# Customize the chart layout
fig_so.update_layout(
    xaxis_title="Response",
    yaxis_title="Count",
    plot_bgcolor='rgba(0,0,0,0)',  # Transparent background
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(color='white'),  # Adjust font color for readability
    showlegend=False  # Hide the legend if not necessary
)

# Customize bar appearance
fig_so.update_traces(
    marker_line_color='rgb(8,48,107)',  # Dark blue border for bars
    marker_line_width=1.5,  # Width of the border
    opacity=0.8,
    textangle = 0
)
st.plotly_chart(fig_so,use_container_width=True)

# --- end of the chart 

# -- Bar Chart Type of submision 

submit_type = df["What type of submission you made?"].value_counts()

fig_st = px.bar(submit_type, 
                x=submit_type.index,
                y=submit_type.values,
                text_auto=True,  # Automatically add text on bars
                title='What type of submission you made?',
                color = submit_type.index,
                 color_discrete_sequence=px.colors.sequential.RdBu_r  # Use a blue color scale consistent with other charts
                 )
# Customize the chart layout
fig_st.update_layout(
    xaxis_title="Response",
    yaxis_title="Count",
    plot_bgcolor='rgba(0,0,0,0)',  # Transparent background
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(color='white'),  # Adjust font color for readability
    showlegend=False  # Hide the legend if not necessary
)

# Customize bar appearance
fig_st.update_traces(
    marker_line_color='rgb(8,48,107)',  # Dark blue border for bars
    marker_line_width=1.5,  # Width of the border
    opacity=0.8,
    textangle = 0
)

st.plotly_chart(fig_st, use_container_width=True)

# --- end of the chart 
st.markdown('---')
# -- Pie Chart 

# Calculate the counts for each age group
followup_count = df['Did anyone from INTERSOS reached out to you after your complaint/feedback?'].value_counts()

# Create the pie chart with a blue color scheme
fig_flup = px.pie(
    followup_count,
    values=followup_count.values,
    names=followup_count.index,
    title='Did anyone from INTERSOS reached out to you after your complaint/feedback?',
    color_discrete_sequence=px.colors.sequential.RdBu_r  # Set the color scheme to blue
)

# Customize layout for clarity and visibility
fig_flup.update_traces(
    textinfo='percent+label',
    marker=dict(line=dict(color='#000000', width=2))  # Adds a line around each segment
)

# Set transparent background
fig_flup.update_layout(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    showlegend=True
)

st.plotly_chart(fig_flup, use_container_width= True)

# --- end of the chart 
st.markdown('---')
# -- Bar Chart L1

# Sort the DataFrame in the desired order
desired_order = ['Very Good', 'Good', 'Neutral', 'Bad', 'Very Bad']
lq_submitting_sorted = df["How would you rate the experience of submitting a complaint/feedback?"].value_counts().reindex(desired_order)

# Define the custom color sequence
custom_colors = ['blue', 'lightblue', 'gray', 'lightcoral', 'red']

# Create the bar chart
fig_st = px.bar(
    lq_submitting_sorted,
    x=lq_submitting_sorted.index,
    y=lq_submitting_sorted.values,
    text_auto=True,
    title='Experience Rating of Submitting a Complaint/Feedback',
    color=lq_submitting_sorted.index,
    color_discrete_sequence=custom_colors
)

# Customize the chart layout
fig_st.update_layout(
    xaxis_title="Response",
    yaxis_title="Count",
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(color='white'),
    showlegend=False
)

# Customize bar appearance
fig_st.update_traces(
    marker_line_color='rgb(8,48,107)',
    marker_line_width=1.5,
    opacity=0.8,
    textangle=0
)

st.plotly_chart(fig_st, use_container_width=True)

# ----

# Sort the DataFrame in the desired order
desired_order = ['Very Good', 'Good', 'Neutral', 'Bad', 'Very Bad']
lq_submitting_sorted2 = df["How would you rate the speed of INTERSOS reaching to you after your complaint/feedback?"].value_counts().reindex(desired_order)

# Define the custom color sequence
custom_colors = ['blue', 'lightblue', 'gray', 'lightcoral', 'red']

# Create the bar chart
fig_st2 = px.bar(
    lq_submitting_sorted2,
    x=lq_submitting_sorted2.index,
    y=lq_submitting_sorted2.values,
    text_auto=True,
    title='Experience Rating of Receiving Follow Up',
    color=lq_submitting_sorted2.index,
    color_discrete_sequence=custom_colors
)

# Customize the chart layout
fig_st2.update_layout(
    xaxis_title="Response",
    yaxis_title="Count",
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(color='white'),
    showlegend=False
)

# Customize bar appearance
fig_st2.update_traces(
    marker_line_color='rgb(8,48,107)',
    marker_line_width=1.5,
    opacity=0.8,
    textangle=0
)

st.plotly_chart(fig_st2,use_container_width=True)

# Sort the DataFrame in the desired order
desired_order = ['Very Good', 'Good', 'Neutral', 'Bad', 'Very Bad']
lq_submitting_sorted3 = df["How would you rate the experience of receiving updates on your case?"].value_counts().reindex(desired_order)

# Define the custom color sequence
custom_colors = ['blue', 'lightblue', 'gray', 'lightcoral', 'red']

# Create the bar chart
fig_st3 = px.bar(
    lq_submitting_sorted3,
    x=lq_submitting_sorted3.index,
    y=lq_submitting_sorted3.values,
    text_auto=True,
    title='Experience Rating of receiving updates',
    color=lq_submitting_sorted3.index,
    color_discrete_sequence=custom_colors
)

# Customize the chart layout
fig_st3.update_layout(
    xaxis_title="Response",
    yaxis_title="Count",
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(color='white'),
    showlegend=False
)

# Customize bar appearance
fig_st3.update_traces(
    marker_line_color='rgb(8,48,107)',
    marker_line_width=1.5,
    opacity=0.8,
    textangle=0
)

st.plotly_chart(fig_st3, use_container_width=True)

# Sort the DataFrame in the desired order
desired_order = ['Very Good', 'Good', 'Neutral', 'Bad', 'Very Bad']
lq_submitting_sorted4= df["How would you rate INTERSOS' attempt to implement your complaint/feedback?"].value_counts().reindex(desired_order)

# Define the custom color sequence
custom_colors = ['blue', 'lightblue', 'gray', 'lightcoral', 'red']

# Create the bar chart
fig_st4 = px.bar(
    lq_submitting_sorted4,
    x=lq_submitting_sorted4.index,
    y=lq_submitting_sorted4.values,
    text_auto=True,
    title='Experience Rating of implementation of complaint/feedback',
    color=lq_submitting_sorted4.index,
    color_discrete_sequence=custom_colors
)

# Customize the chart layout
fig_st4.update_layout(
    xaxis_title="Response",
    yaxis_title="Count",
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(color='white'),
    showlegend=False
)

# Customize bar appearance
fig_st4.update_traces(
    marker_line_color='rgb(8,48,107)',
    marker_line_width=1.5,
    opacity=0.8,
    textangle=0
)

st.plotly_chart(fig_st4, use_container_width=True)


# ------ section ends 

st.markdown('---')

df['Did INTERSOS staff follow up with you to provide updates on the status of your case? Informing about updates, timelines, etc.'].replace({
    'Yes, I received regular and comprehensive updates regarding the status of my complaint.': 'Regular Updates',
    'I received moderate communication and updates about my issue.': 'Moderate Communication',
    'No follow-up or status updates were provided after the initial call.': 'No Follow-up',
    "I haven't received an initial call.": 'No Initial Call'
}, inplace=True)

# Calculate the counts for each age group
followup_aftercall = df['Did INTERSOS staff follow up with you to provide updates on the status of your case? Informing about updates, timelines, etc.'].value_counts()

# Create the bar chart with a consistent color scheme
fig_follow_up_aftercall = px.bar(
    followup_aftercall,
    x=followup_aftercall.index,
    y=followup_aftercall.values,
    text_auto=True,  # Automatically add text on bars
    title='Received follow up updates',
    color = followup_aftercall.index,
    color_discrete_sequence=px.colors.sequential.RdBu_r  # Use a blue color scale consistent with other charts
)

# Customize the chart layout
fig_follow_up_aftercall.update_layout(
    xaxis_title="Response",
    yaxis_title="Count",
    plot_bgcolor='rgba(0,0,0,0)',  # Transparent background
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(color='white'),  # Adjust font color for readability
    showlegend=False  # Hide the legend if not necessary
)

# Customize bar appearance
fig_follow_up_aftercall.update_traces(
    marker_line_color='rgb(8,48,107)',  # Dark blue border for bars
    marker_line_width=1.5,  # Width of the border
    opacity=0.8  # Adjust for slight transparency
)

st.plotly_chart(fig_follow_up_aftercall, use_container_width=True)

# -- end chart 

st.markdown('---')

# --- Bar Chart Resolution 

df['Do you think that the INTERSOS\' Complaint, Feedback and Response Mechanisms (CFRM) has had a positive impact on your complaint/feedback?'].replace({
    'Yes, all my complaints/feedback were taken into account': 'All Addressed',
    'Some of my complaints/feedback were taken into account': 'Some Addressed',
    'No changes followed my complaint/feedback': 'No Changes'
}, inplace=True)

# Calculate the counts for each age group
complaint_resolution = df['Do you think that the INTERSOS\' Complaint, Feedback and Response Mechanisms (CFRM) has had a positive impact on your complaint/feedback?'].value_counts()

# Create the bar chart with a consistent color scheme
fig_complaint_res = px.bar(
    complaint_resolution,
    x=complaint_resolution.index,
    y=complaint_resolution.values,
    text_auto=True,  # Automatically add text on bars
    title='Complaint Resolution Chart',
    color = complaint_resolution.index,
    color_discrete_sequence=px.colors.sequential.RdBu_r  # Use a blue color scale consistent with other charts
)

# Customize the chart layout
fig_complaint_res.update_layout(
    xaxis_title="Response",
    yaxis_title="Count",
    plot_bgcolor='rgba(0,0,0,0)',  # Transparent background
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(color='white'),  # Adjust font color for readability
    showlegend=False  # Hide the legend if not necessary
)

# Customize bar appearance
fig_complaint_res.update_traces(
    marker_line_color='rgb(8,48,107)',  # Dark blue border for bars
    marker_line_width=1.5,  # Width of the border
    opacity=0.8  # Adjust for slight transparency
)

st.plotly_chart(fig_complaint_res, use_container_width=True)

# -- Chart 

# Calculate the counts for each age group
comp_res_opinion = df['Do you feel like INTERSOS did their best to implement your complaint/feedback?'].value_counts()

# Create the pie chart with a blue color scheme
fig_cr_opinion = px.pie(
    comp_res_opinion,
    values=comp_res_opinion.values,
    names=comp_res_opinion.index,
    title='Do you feel like INTERSOS did their best to implement your complaint/feedback?',
    color_discrete_sequence=px.colors.sequential.RdBu_r  # Set the color scheme to blue
)

# Customize layout for clarity and visibility
fig_cr_opinion.update_traces(
    textinfo='percent+label',
    marker=dict(line=dict(color='#000000', width=2))  # Adds a line around each segment
)

# Set transparent background
fig_cr_opinion.update_layout(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    showlegend=True
)

st.plotly_chart(fig_cr_opinion, use_container_width=True)


st.markdown('---')

# -- Communication Sequence 

contact_methods = [
    "Email;",
    "Online form;",
    "Feedback box;",
    "Hotline;",
    "In person;",
    "Viber;",
    "Telegram;",
    "Whatsapp;",
    "Facebook/Messengers;",
    "Other;"
]

contact_methods_c = df['What would be the preferred channel of communication for a non-sensitive matter?']
contact_methods_counts = {answer: contact_methods_c.str.count(answer).sum() for answer in contact_methods}

df_com_nonsens = pd.DataFrame(list(contact_methods_counts.items()), columns=['Answer', 'Count'])

# Sort data for better visualization
df_com_nonsens_sorted = df_com_nonsens.sort_values('Count', ascending=False)


# Create the bar chart with simplified x-axis
fig_com_nonsens = px.bar(
    df_com_nonsens_sorted,
    x='Answer',
    y='Count',
    text_auto=True,  # Automatically add text on bars
    title='Prefered Communication Channels (Non-sensetive)',
    color='Answer',  # Color by answer
    color_continuous_scale='blues'  # Use a blue color scale
)

# Customize the chart layout
fig_com_nonsens.update_layout(
    xaxis_title="",
    yaxis_title="Count",
    plot_bgcolor='rgba(0,0,0,0)',  # Transparent background
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(color='white'),  # Adjust font color for readability
    showlegend=True  # Ensure the legend is shown
)

# Customize x-axis to remove the labels
fig_com_nonsens.update_xaxes(showticklabels=False)  # Hide x-axis labels

# Customize bar appearance
fig_com_nonsens.update_traces(
    marker_line_color='rgb(8,48,107)',  # Dark blue border for bars
    marker_line_width=1.5,  # Width of the border
    opacity=0.8  # Adjust for slight transparency
)

st.plotly_chart(fig_com_nonsens, use_container_width=True)
# -------
contact_methods_c = df['What would be the preferred channel of communication for a sensitive matter?']
contact_methods_counts = {answer: contact_methods_c.str.count(answer).sum() for answer in contact_methods}

df_com_nonsens = pd.DataFrame(list(contact_methods_counts.items()), columns=['Answer', 'Count'])

# Sort data for better visualization
df_com_nonsens_sorted = df_com_nonsens.sort_values('Count', ascending=False)


# Create the bar chart with simplified x-axis
fig_com_sens = px.bar(
    df_com_nonsens_sorted,
    x='Answer',
    y='Count',
    text_auto=True,  # Automatically add text on bars
    title='Prefered Communication Channels (Sensetive)',
    color='Answer',  # Color by answer
    color_continuous_scale='blues'  # Use a blue color scale
)

# Customize the chart layout
fig_com_sens.update_layout(
    xaxis_title="",
    yaxis_title="Count",
    plot_bgcolor='rgba(0,0,0,0)',  # Transparent background
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(color='white'),  # Adjust font color for readability
    showlegend=True  # Ensure the legend is shown
)

# Customize x-axis to remove the labels
fig_com_sens.update_xaxes(showticklabels=False)  # Hide x-axis labels

# Customize bar appearance
fig_com_sens.update_traces(
    marker_line_color='rgb(8,48,107)',  # Dark blue border for bars
    marker_line_width=1.5,  # Width of the border
    opacity=0.8,
    textangle = 0
)

# Show the figure
st.plotly_chart(fig_com_sens, use_container_width=True)

st.markdown('---')

# --- Feedback charts


improvements1 = [
    "Improved communication channels;",
    "Better placement of the CFRM box;",
    "Faster response times;",
    "Improved transparency;",
    "Improved communication about the case;",
    "Other;"
]


improvements1_c = df['What are the areas you would like to see improved in the INTERSOS\' Complaint, Feedback and Response Mechanisms(CFRM)?']
improvements1_counts = {answer: improvements1_c.str.count(answer).sum() for answer in improvements1}

df_improve_cfrm = pd.DataFrame(list(improvements1_counts.items()), columns=['Answer', 'Count'])

# Sort data for better visualization
df_improve_cfrm_sorted = df_improve_cfrm.sort_values('Count', ascending=False)


# Create the bar chart with simplified x-axis
fig_improve_cfrm = px.bar(
    df_improve_cfrm_sorted,
    x='Answer',
    y='Count',
    text_auto=True,  # Automatically add text on bars
    title='Key Aspects to Improve',
    color='Answer',  # Color by answer
    color_continuous_scale='blues'  # Use a blue color scale
)

# Customize the chart layout
fig_improve_cfrm.update_layout(
    xaxis_title="",
    yaxis_title="Count",
    plot_bgcolor='rgba(0,0,0,0)',  # Transparent background
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(color='white'),  # Adjust font color for readability
    showlegend=True  # Ensure the legend is shown
)

# Customize x-axis to remove the labels
fig_improve_cfrm.update_xaxes(showticklabels=False)  # Hide x-axis labels

# Customize bar appearance
fig_improve_cfrm.update_traces(
    marker_line_color='rgb(8,48,107)',  # Dark blue border for bars
    marker_line_width=1.5,  # Width of the border
    opacity=0.8,
    textangle = 0
)

# Show the figure
st.plotly_chart(fig_improve_cfrm, use_container_width=True)


improvements1 = [
    "Privacy;",
    "Safety;",
    "Good communication channels;",
    "Effectiveness;",
    "Responsiveness;",
    "Other;"
]


improvements1_c = df['What are the most important elements of complaint system that would encourage you to use it?']
improvements1_counts = {answer: improvements1_c.str.count(answer).sum() for answer in improvements1}

df_improve_cfrm = pd.DataFrame(list(improvements1_counts.items()), columns=['Answer', 'Count'])

# Sort data for better visualization
df_improve_cfrm_sorted = df_improve_cfrm.sort_values('Count', ascending=False)


# Create the bar chart with simplified x-axis
fig_improve_overall = px.bar(
    df_improve_cfrm_sorted,
    x='Answer',
    y='Count',
    text_auto=True,  # Automatically add text on bars
    title='Key Aspects that encourage usage',
    color='Answer',  # Color by answer
    color_continuous_scale='blues'  # Use a blue color scale
)

# Customize the chart layout
fig_improve_overall.update_layout(
    xaxis_title="",
    yaxis_title="Count",
    plot_bgcolor='rgba(0,0,0,0)',  # Transparent background
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(color='white'),  # Adjust font color for readability
    showlegend=True  # Ensure the legend is shown
)

# Customize x-axis to remove the labels
fig_improve_overall.update_xaxes(showticklabels=False)  # Hide x-axis labels

# Customize bar appearance
fig_improve_overall.update_traces(
    marker_line_color='rgb(8,48,107)',  # Dark blue border for bars
    marker_line_width=1.5,  # Width of the border
    opacity=0.8,
    textangle = 0
)

# Show the figure
st.plotly_chart(fig_improve_overall, use_container_width=True)

feedback_categories  = [
    "Suggestion of improvement of INTERSOS services;",
    "Behavior of INTERSOS staff;",
    "Information regarding INTERSOS' services;",
    "Complaint about the quality of INTERSOS' services;",
    "Safety concerns regarding the current accommodation;",
    "Other;"
]


feedback_cat = df['If you had to make a complaint or suggestion, what topic would it cover?']
feedback_cat_count = {answer: feedback_cat.str.count(answer).sum() for answer in feedback_categories }

df_improve_cfrm = pd.DataFrame(list(feedback_cat_count.items()), columns=['Answer', 'Count'])

# Sort data for better visualization
df_improve_cfrm_sorted = df_improve_cfrm.sort_values('Count', ascending=False)


# Create the bar chart with simplified x-axis
fig_complaint_topic_now = px.bar(
    df_improve_cfrm_sorted,
    x='Answer',
    y='Count',
    text_auto=True,  # Automatically add text on bars
    title='Blitz Complaint Topic',
    color='Answer',  # Color by answer
    color_continuous_scale='blues'  # Use a blue color scale
)

# Customize the chart layout
fig_complaint_topic_now.update_layout(
    xaxis_title="",
    yaxis_title="Count",
    plot_bgcolor='rgba(0,0,0,0)',  # Transparent background
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(color='white'),  # Adjust font color for readability
    showlegend=True  # Ensure the legend is shown
)

# Customize x-axis to remove the labels
fig_complaint_topic_now.update_xaxes(showticklabels=False)  # Hide x-axis labels

# Customize bar appearance
fig_complaint_topic_now.update_traces(
    marker_line_color='rgb(8,48,107)',  # Dark blue border for bars
    marker_line_width=1.5,  # Width of the border
    opacity=0.8,
    textangle = 0
)

# Show the figure
st.plotly_chart(fig_complaint_topic_now, use_container_width=True)

