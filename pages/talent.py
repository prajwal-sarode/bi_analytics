from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
from config import TEXT_MAIN
from plots.talent_plots import plot_top_skills, plot_exp_by_grade

def render_talent(dff):
    # Columns to show in the table
    table_cols = ['Emp_ID', 'Name', 'Role', 'Grade', 'Shift', 'Compliance_Score', 'City']
    
    return html.Div([
        html.H2("Workforce Analytics", className="h-title"),
        dbc.Row([
            dbc.Col(html.Div([
                html.H5("Top Skills Inventory", className="mb-3"), 
                dcc.Graph(figure=plot_top_skills(dff))
            ], className="custom-card"), width=6),
            dbc.Col(html.Div([
                html.H5("Experience Ranges by Grade", className="mb-3"), 
                dcc.Graph(figure=plot_exp_by_grade(dff))
            ], className="custom-card"), width=6)
        ]),
        html.H3("Detailed Roster", className="h-title mt-4"),
        html.Div([
            dash_table.DataTable(
                data=dff.to_dict('records'),
                columns=[{'name': i.replace('_', ' '), 'id': i} for i in table_cols],
                page_size=10,
                sort_action='native',
                filter_action='native',
                style_header={'backgroundColor': '#F8FAFC', 'fontWeight': 'bold', 'borderBottom': '2px solid #E2E8F0', 'color': TEXT_MAIN},
                style_cell={'textAlign': 'left', 'padding': '12px', 'fontFamily': 'Inter', 'borderBottom': '1px solid #E2E8F0', 'color': TEXT_MAIN},
                style_data_conditional=[{'if': {'row_index': 'odd'}, 'backgroundColor': '#F8FAFC'}]
            )
        ], className="custom-card")
    ])