import plotly.express as px
from config import PRIMARY, SECONDARY, ACCENT, SUCCESS
from utils.plotting import clean_layout

def plot_role_distribution(df):
    role_counts = df['Role'].value_counts().reset_index()
    role_counts.columns = ['Role', 'Count']
    fig = px.bar(role_counts, x='Count', y='Role', orientation='h', text='Count', 
                 color='Count', color_continuous_scale='Blues')
    fig.update_layout(coloraxis_showscale=False, yaxis={'categoryorder':'total ascending'})
    return clean_layout(fig, height=280)

def plot_gender_split(df, total_hc):
    fig = px.pie(df, names='Gender', hole=0.7, color_discrete_sequence=[PRIMARY, SECONDARY])
    fig.update_layout(annotations=[dict(text=f"{total_hc}", x=0.5, y=0.5, font_size=20, showarrow=False)])
    return clean_layout(fig, height=280)

def plot_experience_hist(df):
    fig = px.histogram(df, x='Total_Experience', nbins=15, color_discrete_sequence=[ACCENT])
    fig.update_layout(xaxis_title="Years Experience", yaxis_title="Staff Count")
    return clean_layout(fig, height=280)

def plot_software_adoption(df):
    sw_counts = df.groupby(['Role', 'Software_User']).size().reset_index(name='Count')
    fig = px.bar(sw_counts, x='Role', y='Count', color='Software_User', barmode='stack', 
                    color_discrete_map={'Yes': SUCCESS, 'No': '#E2E8F0'})
    return clean_layout(fig, height=280)