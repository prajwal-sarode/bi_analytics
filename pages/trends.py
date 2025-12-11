# pages/trends.py
from dash import html, dcc
import dash_bootstrap_components as dbc
from plots.trend_plots import (
    plot_hiring_trend, 
    plot_attrition_by_grade, 
    plot_attrition_by_dept, 
    plot_tenure_risk,
    plot_top_exit_sites  # <-- New Import
)

def render_trends(dff):
    return html.Div([
        html.H2("Growth & Attrition Trends", className="h-title"),
        
        # ROW 1: Timeline
        dbc.Row([
            dbc.Col(html.Div([
                html.H5("Monthly Hiring vs. Exits", className="mb-3"), 
                dcc.Graph(figure=plot_hiring_trend(dff))
            ], className="custom-card"), width=12)
        ]),

        # ROW 2: Dept, Grade, and Top Exit Sites
        dbc.Row([
            dbc.Col(html.Div([
                html.H5("Attrition by Department", className="mb-3"), 
                dcc.Graph(figure=plot_attrition_by_dept(dff))
            ], className="custom-card"), width=4),
            
            dbc.Col(html.Div([
                html.H5("Attrition by Grade", className="mb-3"), 
                dcc.Graph(figure=plot_attrition_by_grade(dff))
            ], className="custom-card"), width=4),

            # REPLACED COMPONENT HERE
            dbc.Col(html.Div([
                html.H5("Sites with Highest Attrition", className="mb-3"), 
                html.P("Top 5 sites with the most resignations.", 
                       style={'fontSize': '0.75rem', 'color': '#64748B', 'marginBottom': '10px'}),
                dcc.Graph(figure=plot_top_exit_sites(dff))
            ], className="custom-card"), width=4),
        ]),

        # ROW 3: Tenure
        dbc.Row([
            dbc.Col(html.Div([
                html.H5("Tenure Risk Analysis (When do they resign?)", className="mb-3"), 
                html.P("Clusters on the left indicate 'Early Churn' issues (bad hiring/onboarding).", 
                       style={'fontSize': '0.8rem', 'color': '#64748B'}),
                dcc.Graph(figure=plot_tenure_risk(dff))
            ], className="custom-card"), width=12)
        ])
    ])