from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import sys
from app import app
server = app.server
from data.engine import load_data
from components.sidebar import create_sidebar
from config import BG_COLOR, CARD_BG, TEXT_MAIN, TEXT_SUB, PRIMARY, SIDEBAR_BG

# Import Pages
from pages import overview, sites, trends, talent

# 1. Load Data
df, geojson_data = load_data()
unique_zones = df['Zone'].unique()
unique_grades = df['Grade'].unique()

# 2. Main Layout Shell
app.layout = html.Div([
    dcc.Location(id="url"), 
    create_sidebar(unique_zones, unique_grades), 
    html.Div(id="page-content", className="content")
])

# 3. Add Custom CSS (Inline for simplicity, or move to assets/style.css)
app.index_string = f'''
<!DOCTYPE html>
<html>
    <head>
        {{%metas%}}
        <title>{{%title%}}</title>
        {{%favicon%}}
        {{%css%}}
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
        <style>
            html, body {{ background-color: {BG_COLOR}; color: {TEXT_MAIN}; font-family: 'Inter', sans-serif; overflow-x: hidden; }}
            .sidebar {{ position: fixed; top: 0; left: 0; bottom: 0; width: 16rem; padding: 2rem 1rem; background: {SIDEBAR_BG}; box-shadow: 4px 0 24px rgba(0,0,0,0.02); z-index: 1000; border-right: 1px solid #E2E8F0; overflow-y: auto; }}
            .content {{ margin-left: 16rem; padding: 2rem; min-height: 100vh; }}
            .nav-link {{ color: {TEXT_SUB} !important; font-weight: 500; margin-bottom: 8px; border-radius: 8px; padding: 10px 15px; }}
            .nav-link:hover {{ background-color: #F1F5F9; color: {PRIMARY} !important; }}
            .nav-link.active {{ background-color: {PRIMARY}; color: white !important; font-weight: 600; box-shadow: 0 4px 12px rgba(37, 99, 235, 0.2); }}
            .custom-card {{ background-color: {CARD_BG}; border-radius: 12px; border: 1px solid #E2E8F0; box-shadow: 0 1px 3px rgba(0,0,0,0.05); padding: 20px; margin-bottom: 24px; }}
            .kpi-title {{ font-size: 0.75rem; color: {TEXT_SUB}; text-transform: uppercase; letter-spacing: 0.05em; font-weight: 600; }}
            .kpi-value {{ font-size: 2rem; font-weight: 700; color: {TEXT_MAIN}; margin-top: 4px; }}
            .h-title {{ font-weight: 800; color: {TEXT_MAIN}; letter-spacing: -0.5px; margin-bottom: 20px; }}
            .js-plotly-plot .plotly .modebar {{ display: none !important; }}
        </style>
    </head>
    <body>
        {{%app_entry%}}
        <footer>{{%config%}}{{%scripts%}}{{%renderer%}}</footer>
    </body>
</html>
'''

# 4. Global Callback
@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname"), Input("zone-filter", "value"), Input("grade-filter", "value")]
)
def display_page(pathname, sel_zones, sel_grades):
    print(f"DEBUG: Pathname received: {pathname}", file=sys.stderr)
    sys.stderr.flush()
    # Filter Data Global Logic
    dff = df.copy()
    if sel_zones: dff = dff[dff['Zone'].isin(sel_zones)]
    if sel_grades: dff = dff[dff['Grade'].isin(sel_grades)]

    if pathname == "/" or pathname is None:
        return overview.render_overview(dff)
    elif pathname == "/sites":
        # Note: You'd pass geojson_data here if you implement it in site_plots
        return sites.render_sites(dff, geojson_data) 
    elif pathname == "/trends":
        return trends.render_trends(dff)
    elif pathname == "/talent":
        return talent.render_talent(dff)
    else:
        return html.Div("404 Page Not Found")

if __name__ == "__main__":
    app.run(debug=True, port=8000)