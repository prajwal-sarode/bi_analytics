import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from config import PRIMARY, SECONDARY, ACCENT, SUCCESS, TEXT_MAIN
from utils.plotting import clean_layout

# --- 1. CONFIGURATION ---

# Defined Palette: Grouped by STATE
STATE_COLOR_MAP = {
    'Maharashtra': '#6366F1',     # Indigo
    'Karnataka': '#EC4899',       # Pink
    'Haryana': '#F59E0B',         # Amber
    'Delhi': '#EF4444',           # Red
    'Tamil Nadu': '#10B981',      # Emerald
    'Telangana': '#3B82F6',       # Blue
    'West Bengal': '#14B8A6',     # Teal
    'Gujarat': '#F97316',         # Orange
    'Uttar Pradesh': '#84CC16',   # Lime
    'Rajasthan': '#EAB308'        # Yellow
}

# Map Cities to their State Colors
CITY_COLOR_MAP = {
    'Mumbai': STATE_COLOR_MAP['Maharashtra'],
    'Pune': STATE_COLOR_MAP['Maharashtra'],
    'Nagpur': STATE_COLOR_MAP['Maharashtra'],
    'Bangalore': STATE_COLOR_MAP['Karnataka'],
    'Mysore': STATE_COLOR_MAP['Karnataka'],
    'Gurugram': STATE_COLOR_MAP['Haryana'],
    'Manesar': STATE_COLOR_MAP['Haryana'],
    'New Delhi': STATE_COLOR_MAP['Delhi'],
    'Delhi': STATE_COLOR_MAP['Delhi'],
    'Chennai': STATE_COLOR_MAP['Tamil Nadu'],
    'Coimbatore': STATE_COLOR_MAP['Tamil Nadu'],
    'Hyderabad': STATE_COLOR_MAP['Telangana'],
    'Kolkata': STATE_COLOR_MAP['West Bengal'],
    'Ahmedabad': STATE_COLOR_MAP['Gujarat'],
    'Vadodara': STATE_COLOR_MAP['Gujarat'],
    'Noida': STATE_COLOR_MAP['Uttar Pradesh']
}
DEFAULT_COLOR = "#64748B"

def hex_to_rgba(hex_code, opacity):
    hex_code = hex_code.lstrip('#')
    return f"rgba({int(hex_code[0:2], 16)},{int(hex_code[2:4], 16)},{int(hex_code[4:6], 16)},{opacity})"

# --- 2. THE CONNECTED MAP & BARS ---

def plot_geo_map(df, geojson_data=None):
    """
    Choropleth Map: Highlights the REGION (State).
    """
    # Aggregate by State
    state_counts = df.groupby('State')['Emp_ID'].count().reset_index(name='Count')
    
    # Assign Colors explicitly
    state_counts['Color'] = state_counts['State'].map(STATE_COLOR_MAP).fillna(DEFAULT_COLOR)

    # --- FIX IS HERE: Explicit check 'is not None' ---
    if geojson_data is not None:
        fig = px.choropleth_mapbox(
            state_counts,
            geojson=geojson_data,
            locations='State',
            featureidkey="properties.NAME_1",
            color='State',
            color_discrete_map=STATE_COLOR_MAP,
            hover_name='State',
            hover_data={'State': False, 'Count': True},
            zoom=3.2,
            center={"lat": 22, "lon": 82},
            opacity=0.7
        )
        fig.update_layout(mapbox_style="carto-positron", margin={'r':0,'t':0,'l':0,'b':0}, showlegend=False)
    else:
        # Fallback if GeoJSON fails
        fig = px.scatter_geo(state_counts, locations='State', locationmode="country names", size='Count')
        fig.update_layout(title="Map Data Unavailable")

    return fig

def plot_top_sites_horizontal(df):
    """
    Horizontal Bars colored by City (matches State color).
    """
    # Group by Site & City
    site_counts = df.groupby(['Site_Name', 'City'])['Emp_ID'].count().reset_index(name='Count')
    site_counts = site_counts.sort_values('Count', ascending=False).head(10) 
    site_counts = site_counts.sort_values('Count', ascending=True)

    fig = px.bar(
        site_counts, 
        y='Site_Name', 
        x='Count', 
        orientation='h', 
        text='Count',
        color='City', 
        color_discrete_map=CITY_COLOR_MAP # Matches the Map colors
    )
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font={'family': "Inter", 'color': TEXT_MAIN, 'size': 11},
        margin=dict(l=0, r=0, t=10, b=0), bargap=0.15,
        xaxis=dict(showgrid=False, showticklabels=False, title=None),
        yaxis=dict(showgrid=False, title=None, ticksuffix=" "),
        showlegend=False
    )
    fig.update_traces(textposition='inside', textfont_color='white', textfont_weight='bold')
    return fig

# --- 3. THE SANKEY DIAGRAM (HIERARCHY) ---

def plot_org_treemap(df):
    """
    Sankey Diagram for Zone > Site Flow
    """
    df_grouped = df.groupby(['Zone', 'Site_Name'])['Emp_ID'].count().reset_index(name='Count')
    
    zones = list(df_grouped['Zone'].unique())
    sites = list(df_grouped['Site_Name'].unique())
    all_nodes = zones + sites
    
    sources = [zones.index(z) for z in df_grouped['Zone']]
    targets = [len(zones) + sites.index(s) for s in df_grouped['Site_Name']]
    values = df_grouped['Count'].tolist()

    # Zone Colors
    zone_color_map = {'North': PRIMARY, 'South': SECONDARY, 'West': ACCENT, 'East': SUCCESS}
    
    # Node Colors
    node_colors = [zone_color_map.get(z, '#94A3B8') for z in zones] + ['#CBD5E1'] * len(sites)
    
    # Link Colors (Transparent)
    link_colors = []
    for z in df_grouped['Zone']:
        base_hex = zone_color_map.get(z, '#94A3B8')
        link_colors.append(hex_to_rgba(base_hex, 0.4))

    fig = go.Figure(data=[go.Sankey(
        node = dict(pad=15, thickness=20, line=dict(color="white", width=0.5), label=all_nodes, color=node_colors),
        link = dict(source=sources, target=targets, value=values, color=link_colors)
    )])

    fig.update_layout(
        font=dict(size=10, color="#1E293B", family="Inter"),
        margin=dict(l=10, r=10, t=10, b=10), height=450,
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)'
    )
    return fig

# --- 4. CRITICAL SITES ---

def plot_critical_sites(df):
    """
    Simple Bar Chart for Critical Sites
    """
    hp_sites = df[df['Is_High_Profile'] == True]['Site_Name'].value_counts().nlargest(5).reset_index()
    hp_sites.columns = ['Site', 'Count']
    fig = px.bar(hp_sites, x='Count', y='Site', orientation='h', text='Count')
    fig.update_traces(marker_color=ACCENT)
    return clean_layout(fig, height=300)





# # plots/site_plots.py
# import plotly.express as px
# import plotly.graph_objects as go
# import pandas as pd
# from config import PRIMARY, SECONDARY, ACCENT, SUCCESS, TEXT_MAIN
# from utils.plotting import clean_layout

# TEAL_COLOR = "#0D9488" 

# def hex_to_rgba(hex_code, opacity):
#     hex_code = hex_code.lstrip('#')
#     return f"rgba({int(hex_code[0:2], 16)},{int(hex_code[2:4], 16)},{int(hex_code[4:6], 16)},{opacity})"

# def plot_geo_map(df, geojson_data=None):
#     """
#     Bubble Map
#     """
#     city_counts = df.groupby(['City', 'State'])['Emp_ID'].count().reset_index(name='Count')

#     # Hardcoded Lat/Lon
#     coords = {
#         'Mumbai': {'lat': 19.0760, 'lon': 72.8777}, 'Pune': {'lat': 18.5204, 'lon': 73.8567},
#         'Nagpur': {'lat': 21.1458, 'lon': 79.0882}, 'Bangalore': {'lat': 12.9716, 'lon': 77.5946},
#         'Mysore': {'lat': 12.2958, 'lon': 76.6394}, 'Chennai': {'lat': 13.0827, 'lon': 80.2707},
#         'Coimbatore': {'lat': 11.0168, 'lon': 76.9558}, 'Hyderabad': {'lat': 17.3850, 'lon': 78.4867},
#         'New Delhi': {'lat': 28.6139, 'lon': 77.2090}, 'Delhi': {'lat': 28.6139, 'lon': 77.2090},
#         'Gurugram': {'lat': 28.4595, 'lon': 77.0266}, 'Manesar': {'lat': 28.3515, 'lon': 76.9428},
#         'Ahmedabad': {'lat': 23.0225, 'lon': 72.5714}, 'Vadodara': {'lat': 22.3072, 'lon': 73.1812},
#         'Kolkata': {'lat': 22.5726, 'lon': 88.3639}
#     }

#     city_counts['lat'] = city_counts['City'].map(lambda x: coords.get(x, {}).get('lat'))
#     city_counts['lon'] = city_counts['City'].map(lambda x: coords.get(x, {}).get('lon'))
#     city_counts = city_counts.dropna(subset=['lat', 'lon'])

#     fig = px.scatter_mapbox(
#         city_counts, lat="lat", lon="lon", size="Count", 
#         color_discrete_sequence=[TEAL_COLOR],
#         hover_name="City", size_max=35, zoom=3.2, 
#         center={"lat": 21.5, "lon": 82}
#     )
#     fig.update_layout(mapbox_style="carto-positron", margin={'r':0,'t':0,'l':0,'b':0})
#     return fig

# def plot_top_sites_horizontal(df):
#     """
#     New: Horizontal Teal Bars for side-by-side view
#     """
#     site_counts = df['Site_Name'].value_counts().nlargest(10).reset_index()
#     site_counts.columns = ['Site', 'Count']
#     site_counts = site_counts.sort_values('Count', ascending=True)

#     fig = px.bar(site_counts, y='Site', x='Count', orientation='h', text='Count',
#                  color_discrete_sequence=[TEAL_COLOR])
    
#     fig.update_layout(
#         paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
#         font={'family': "Inter", 'color': TEXT_MAIN, 'size': 11},
#         margin=dict(l=0, r=0, t=10, b=0), bargap=0.2,
#         xaxis=dict(showgrid=False, showticklabels=False, title=None),
#         yaxis=dict(showgrid=False, title=None)
#     )
#     fig.update_traces(textposition='inside', textfont_color='white')
#     return fig

























# # def plot_org_treemap(df):
# #     """
# #     Restored: Aesthetic Sankey Diagram
# #     """
# #     df_grouped = df.groupby(['Zone', 'Site_Name'])['Emp_ID'].count().reset_index(name='Count')
# #     zones = list(df_grouped['Zone'].unique())
# #     sites = list(df_grouped['Site_Name'].unique())
# #     all_nodes = zones + sites
    
# #     sources = [zones.index(z) for z in df_grouped['Zone']]
# #     targets = [len(zones) + sites.index(s) for s in df_grouped['Site_Name']]
# #     values = df_grouped['Count'].tolist()

# #     zone_color_map = {'North': PRIMARY, 'South': SECONDARY, 'West': ACCENT, 'East': SUCCESS}
# #     node_colors = [zone_color_map.get(z, '#94A3B8') for z in zones] + ['#CBD5E1'] * len(sites)
    
# #     link_colors = []
# #     for z in df_grouped['Zone']:
# #         link_colors.append(hex_to_rgba(zone_color_map.get(z, '#94A3B8'), 0.4))

# #     fig = go.Figure(data=[go.Sankey(
# #         node = dict(pad=15, thickness=20, line=dict(color="white", width=0.5), label=all_nodes, color=node_colors),
# #         link = dict(source=sources, target=targets, value=values, color=link_colors)
# #     )])

# #     fig.update_layout(font=dict(size=10, color="#1E293B", family="Inter"), margin=dict(l=10, r=10, t=10, b=10), height=450, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
# #     return fig

# def plot_critical_sites(df):
#     """
#     Restored: Critical High Profile Sites
#     """
#     hp_sites = df[df['Is_High_Profile'] == True]['Site_Name'].value_counts().nlargest(5).reset_index()
#     hp_sites.columns = ['Site', 'Count']
#     fig = px.bar(hp_sites, x='Count', y='Site', orientation='h', text='Count')
#     fig.update_traces(marker_color=ACCENT)
#     return clean_layout(fig, height=300)


# # import plotly.express as px
# # import pandas as pd
# # from config import PRIMARY, SECONDARY, ACCENT, SUCCESS
# # from utils.plotting import clean_layout

# # def plot_geo_map(df, geojson_data=None):
# #     """
# #     Plots a Bubble Map focused on Cities instead of States.
# #     This is more stable and relevant for Facility Management.
# #     """
# #     # 1. Aggregate Data by City
# #     city_counts = df.groupby(['City', 'State'])['Emp_ID'].count().reset_index(name='Count')

# #     # 2. Define Lat/Lon for major FM hubs (Hardcoded for stability)
# #     coords = {
# #         'Mumbai': {'lat': 19.0760, 'lon': 72.8777},
# #         'Pune': {'lat': 18.5204, 'lon': 73.8567},
# #         'Nagpur': {'lat': 21.1458, 'lon': 79.0882},
# #         'Bangalore': {'lat': 12.9716, 'lon': 77.5946},
# #         'Mysore': {'lat': 12.2958, 'lon': 76.6394},
# #         'Chennai': {'lat': 13.0827, 'lon': 80.2707},
# #         'Coimbatore': {'lat': 11.0168, 'lon': 76.9558},
# #         'Hyderabad': {'lat': 17.3850, 'lon': 78.4867},
# #         'New Delhi': {'lat': 28.6139, 'lon': 77.2090},
# #         'Delhi': {'lat': 28.6139, 'lon': 77.2090},
# #         'Gurugram': {'lat': 28.4595, 'lon': 77.0266},
# #         'Manesar': {'lat': 28.3515, 'lon': 76.9428},
# #         'Ahmedabad': {'lat': 23.0225, 'lon': 72.5714},
# #         'Vadodara': {'lat': 22.3072, 'lon': 73.1812},
# #         'Kolkata': {'lat': 22.5726, 'lon': 88.3639}
# #     }

# #     # 3. Map Coordinates to Data
# #     city_counts['lat'] = city_counts['City'].map(lambda x: coords.get(x, {}).get('lat'))
# #     city_counts['lon'] = city_counts['City'].map(lambda x: coords.get(x, {}).get('lon'))
    
# #     # Drop cities we couldn't map (safety check)
# #     city_counts = city_counts.dropna(subset=['lat', 'lon'])

# #     # 4. Create Bubble Map
# #     fig = px.scatter_mapbox(
# #         city_counts, 
# #         lat="lat", lon="lon", 
# #         size="Count", 
# #         color="Count",
# #         hover_name="City",
# #         hover_data={"State": True, "lat": False, "lon": False},
# #         color_continuous_scale="Blues",
# #         size_max=40, 
# #         zoom=3.5, 
# #         center={"lat": 21.5, "lon": 82} # Centered on India
# #     )

# #     fig.update_layout(
# #         mapbox_style="carto-positron",
# #         margin={'r':0,'t':0,'l':0,'b':0}
# #     )
    
# #     return fig

# # def plot_org_treemap(df):
# #     fig = px.treemap(
# #         df, 
# #         path=[px.Constant("All Zones"), 'Zone', 'Site_Name'], 
# #         color='Zone',
# #         color_discrete_map={'North': PRIMARY, 'South': SECONDARY, 'West': ACCENT, 'East': SUCCESS}
# #     )
# #     fig.update_traces(marker=dict(line=dict(width=2, color='#FFFFFF')))
# #     return clean_layout(fig, height=350)

# # def plot_top_sites(df):
# #     # Filter for High Profile (Critical) Sites
# #     hp_sites = df[df['Is_High_Profile'] == True]['Site_Name'].value_counts().nlargest(5).reset_index()
# #     hp_sites.columns = ['Site', 'Count']
# #     fig = px.bar(hp_sites, x='Count', y='Site', orientation='h', text='Count')
# #     fig.update_traces(marker_color=ACCENT)
# #     return clean_layout(fig, height=300)