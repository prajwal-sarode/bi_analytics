# plots/trend_plots.py
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from config import PRIMARY, SECONDARY, DANGER, SUCCESS, ACCENT
from utils.plotting import clean_layout

def plot_hiring_trend(df):
    """
    Line 1: Joined
    Line 2: Exited
    """
    df['Join_Period'] = df['Join_Date'].dt.to_period('M')
    joined_data = df.groupby('Join_Period').size().reset_index(name='Joined')
    joined_data.rename(columns={'Join_Period': 'Month'}, inplace=True)

    resigned_df = df[df['Status'] == 'Resigned'].copy()
    resigned_df = resigned_df.dropna(subset=['Resignation_Date'])
    
    if not resigned_df.empty:
        resigned_df['Exit_Period'] = resigned_df['Resignation_Date'].dt.to_period('M')
        exited_data = resigned_df.groupby('Exit_Period').size().reset_index(name='Exited')
        exited_data.rename(columns={'Exit_Period': 'Month'}, inplace=True)
    else:
        exited_data = pd.DataFrame(columns=['Month', 'Exited'])

    trend_df = pd.merge(joined_data, exited_data, on='Month', how='outer').fillna(0)
    trend_df = trend_df.sort_values('Month')
    trend_df['Month_Str'] = trend_df['Month'].astype(str)

    fig = px.line(
        trend_df, x='Month_Str', y=['Joined', 'Exited'], markers=True,
        color_discrete_map={'Joined': SUCCESS, 'Exited': DANGER}
    )
    fig.update_layout(xaxis_title=None, yaxis_title="Headcount", legend_title=None, hovermode="x unified")
    fig.update_traces(line=dict(width=3))
    return clean_layout(fig, height=350)

def plot_attrition_by_grade(df):
    resigned = df[df['Status'] == 'Resigned']
    if resigned.empty: return go.Figure()
    
    attr_grade = resigned['Grade'].value_counts().reset_index()
    attr_grade.columns = ['Grade', 'Count']
    fig = px.bar(attr_grade, x='Grade', y='Count', color='Grade', text='Count', 
                 color_discrete_sequence=px.colors.sequential.Reds_r)
    return clean_layout(fig, height=300)

def plot_attrition_by_dept(df):
    resigned = df[df['Status'] == 'Resigned']
    if resigned.empty: return go.Figure()

    dept_counts = resigned['Department'].value_counts().reset_index()
    dept_counts.columns = ['Department', 'Count']
    
    fig = px.pie(dept_counts, names='Department', values='Count', hole=0.6,
                 color_discrete_sequence=px.colors.qualitative.Pastel)
    
    total_exits = len(resigned)
    fig.update_layout(annotations=[dict(text=f"{total_exits}", x=0.5, y=0.5, font_size=20, showarrow=False)])
    return clean_layout(fig, height=300)

def plot_tenure_risk(df):
    resigned = df[df['Status'] == 'Resigned']
    if resigned.empty: return go.Figure()

    fig = px.histogram(resigned, x='Tenure_Years', nbins=15, 
                       color_discrete_sequence=[ACCENT], 
                       opacity=0.8)
    fig.update_layout(xaxis_title="Years before Resignation", yaxis_title="Count of Exits", bargap=0.1)
    return clean_layout(fig, height=300)

def plot_top_exit_sites(df):
    """
    NEW PLOT: Shows the specific sites with the highest number of resignations.
    """
    resigned = df[df['Status'] == 'Resigned']
    if resigned.empty: return go.Figure()

    # Get Top 5 Sites by Exits
    site_exits = resigned['Site_Name'].value_counts().nlargest(5).reset_index()
    site_exits.columns = ['Site', 'Exits']

    fig = px.bar(
        site_exits, 
        x='Exits', 
        y='Site', 
        orientation='h', 
        text='Exits'
    )
    
    # Use Danger Color (Red) to indicate warning
    fig.update_traces(marker_color=DANGER)
    
    # Ensure the highest number is at the top
    fig.update_layout(yaxis={'categoryorder':'total ascending'}, xaxis_title=None)
    
    return clean_layout(fig, height=300)