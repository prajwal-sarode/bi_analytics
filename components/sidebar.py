from dash import html, dcc
import dash_bootstrap_components as dbc
from config import PRIMARY, TEXT_SUB, TEXT_MAIN, SIDEBAR_BG

def create_sidebar(zones, grades):
    return html.Div([
        html.Div([
            html.H3("Optick", style={'color': PRIMARY, 'fontWeight': '900', 'letterSpacing': '-1px'}),
            html.Span("Workforce Intelligence", style={'color': TEXT_SUB, 'fontSize': '0.75rem'})
        ], className="mb-5"),
        
        dbc.Nav([
            dbc.NavLink([html.Span("📊", className="me-2"), "Overview"], href="/", active="exact"),
            dbc.NavLink([html.Span("🌏", className="me-2"), "Site Intel"], href="/sites", active="exact"),
            dbc.NavLink([html.Span("📈", className="me-2"), "Trends"], href="/trends", active="exact"),
            dbc.NavLink([html.Span("👥", className="me-2"), "Talent"], href="/talent", active="exact"),
        ], vertical=True, pills=True),

        html.Hr(style={'margin': '2rem 0', 'borderColor': '#E2E8F0'}),
        
        html.Label("Zone Filter", style={'fontWeight': '600', 'fontSize': '0.85rem', 'color': TEXT_MAIN}),
        dcc.Dropdown(id='zone-filter', options=[{'label': z, 'value': z} for z in zones], 
                     multi=True, placeholder="All Zones", className="mb-3"),
        
        html.Label("Grade Filter", style={'fontWeight': '600', 'fontSize': '0.85rem', 'color': TEXT_MAIN}),
        dcc.Dropdown(id='grade-filter', options=[{'label': g, 'value': g} for g in grades], 
                     multi=True, placeholder="All Grades"),
    ], className="sidebar", style={'background': SIDEBAR_BG})