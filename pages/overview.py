from dash import html, dcc
import dash_bootstrap_components as dbc
from components.kpi_card import kpi_widget
from plots.overview_plots import plot_role_distribution, plot_gender_split, plot_experience_hist, plot_software_adoption
from config import PRIMARY, SECONDARY, DANGER, SUCCESS

def render_overview(dff):
    # Logic
    total_hc = len(dff[dff['Status']=='Active'])
    avg_exp = round(dff['Total_Experience'].mean(), 1) if len(dff) > 0 else 0
    attrition = round((len(dff[dff['Status']=='Resigned']) / len(dff)) * 100, 1) if len(dff) > 0 else 0
    sw_adoption = round((len(dff[dff['Software_User']=='Yes']) / len(dff)) * 100, 0) if len(dff) > 0 else 0

    return html.Div([
        html.H2("Executive Dashboard", className="h-title"),
        dbc.Row([
            kpi_widget("Total Headcount", f"{total_hc:,}", "👥", PRIMARY),
            kpi_widget("Avg Experience", f"{avg_exp} Yrs", "🎓", SECONDARY),
            kpi_widget("Attrition Rate", f"{attrition}%", "📉", DANGER),
            kpi_widget("Digital Adoption", f"{sw_adoption}%", "💻", SUCCESS),
        ], className="mb-4"),
        
        dbc.Row([
            dbc.Col(html.Div([html.H5("Workforce by Role", className="mb-3"), dcc.Graph(figure=plot_role_distribution(dff))], className="custom-card"), width=8),
            dbc.Col(html.Div([html.H5("Gender Split", className="mb-3"), dcc.Graph(figure=plot_gender_split(dff, total_hc))], className="custom-card"), width=4)
        ]),
        dbc.Row([
            dbc.Col(html.Div([html.H5("Experience Distribution", className="mb-3"), dcc.Graph(figure=plot_experience_hist(dff))], className="custom-card"), width=6),
            dbc.Col(html.Div([html.H5("Tool Adoption by Role", className="mb-3"), dcc.Graph(figure=plot_software_adoption(dff))], className="custom-card"), width=6)
        ])
    ])