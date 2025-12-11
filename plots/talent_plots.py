import plotly.express as px
from utils.plotting import clean_layout

def plot_top_skills(df):
    # 'Primary_Skill' is the column name in our FM data
    skill_counts = df['Primary_Skill'].value_counts().nlargest(8).reset_index()
    skill_counts.columns = ['Skill', 'Count']
    fig = px.bar(skill_counts, x='Count', y='Skill', orientation='h', text='Count', 
                 color='Count', color_continuous_scale='Teal')
    fig.update_layout(coloraxis_showscale=False)
    return clean_layout(fig)

def plot_exp_by_grade(df):
    fig = px.box(df, x='Grade', y='Total_Experience', color='Grade', 
                 color_discrete_sequence=px.colors.qualitative.Prism)
    fig.update_layout(showlegend=False, yaxis_title="Total Exp (Years)")
    return clean_layout(fig)