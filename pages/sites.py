# pages/sites.py
from dash import html, dcc
import dash_bootstrap_components as dbc
from plots.site_plots import plot_geo_map, plot_top_sites_horizontal,  plot_critical_sites
from config import TEXT_SUB

def render_sites(dff, geojson_data):
    return html.Div([
        html.H2("Site Intelligence", className="h-title"),
        
        # --- ROW 1: Map + Horizontal Bars (The requested Layout) ---
        html.Div([
            html.Div("TOP SITES BY MANPOWER", style={'color': TEXT_SUB, 'fontSize': '0.8rem', 'fontWeight': 'bold', 'marginBottom': '15px', 'letterSpacing': '1px'}),
            
            dbc.Row([
                # Left Side: MAP
                dbc.Col(dcc.Graph(
                    figure=plot_geo_map(dff, geojson_data), 
                    style={'height': '450px', 'borderRadius': '8px', 'overflow': 'hidden'}
                ), width=7, style={'paddingRight': '0'}),
                
                # Right Side: HORIZONTAL BARS
                dbc.Col(html.Div([
                    dcc.Graph(figure=plot_top_sites_horizontal(dff), style={'height': '450px'})
                ], style={'borderLeft': '1px solid #E2E8F0', 'paddingLeft': '15px'}), width=5)
            ])
        ], className="custom-card"),

        # --- ROW 2: Org Hierarchy (Sankey) ---
        # dbc.Row([
        #     dbc.Col(html.Div([
        #         html.H5("Org Hierarchy Flow (Zone > Site)", className="mb-3"), 
        #         dcc.Graph(figure=plot_org_treemap(dff))
        #     ], className="custom-card"), width=12)
        # ]),

        # --- ROW 3: Critical Sites ---
        dbc.Row([
            dbc.Col(html.Div([
                html.H5("Top Critical Sites (High Profile)", className="mb-3"), 
                dcc.Graph(figure=plot_critical_sites(dff))
            ], className="custom-card"), width=12)
        ])
    ])