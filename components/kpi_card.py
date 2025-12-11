import dash_bootstrap_components as dbc
from dash import html

def kpi_widget(title, val, icon, color):
    return dbc.Col(html.Div([
        html.Div([
            html.Div(title, className="kpi-title"),
            html.Div(val, className="kpi-value")
        ]),
        html.Div(icon, style={
            'fontSize': '1.8rem', 'color': color, 
            'background': f"{color}15", 'padding': '12px', 
            'borderRadius': '10px'
        })
    ], className="custom-card d-flex justify-content-between align-items-center"), width=3)