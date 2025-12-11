# utils/plotting.py
from config import TEXT_MAIN

def clean_layout(fig, height=300, bargap=0.3):
    """
    Applies consistent styling to a Plotly figure.
    """
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', 
        plot_bgcolor='rgba(0,0,0,0)',
        font={'family': "Inter", 'color': TEXT_MAIN, 'size': 11},
        margin=dict(l=0, r=0, t=30, b=0),
        xaxis=dict(showgrid=False), 
        yaxis=dict(showgrid=True, gridcolor='#F1F5F9', zeroline=False),
        height=height, 
        bargap=bargap
    )
    return fig