import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="India Data Visualization",
    layout="wide"
)

df = pd.read_csv("india.csv")

st.sidebar.title("India Data Visualization")

states = sorted(df["State"].unique())
states.insert(0, "Overall India")

selected_state = st.sidebar.selectbox(
    "Select State",
    states
)

primary = st.sidebar.selectbox(
    "Bubble Size (Primary Parameter)",
    sorted(df.columns[5:])
)

secondary = st.sidebar.selectbox(
    "Bubble Color (Secondary Parameter)",
    sorted(df.columns[5:])
)

st.sidebar.markdown("### Map Settings")

map_style = st.sidebar.selectbox(
    "Map Style",
    [
        "carto-positron",
        "carto-darkmatter",
        "open-street-map",
        "white-bg"
    ]
)

color_scale = st.sidebar.selectbox(
    "Color Scale",
    [
        "Viridis",
        "Plasma",
        "Cividis",
        "Inferno",
        "Turbo",
        "Blues",
        "Reds"
    ]
)

bubble_multiplier = st.sidebar.slider(
    "Bubble Size Multiplier",
    min_value=1,
    max_value=10,
    value=4
)

show_legend = st.sidebar.checkbox("Show Legend", value=True)

plot = st.sidebar.button("Plot Map")

st.markdown(
    "<h1 style='text-align:center;'>India District-Level Map Visualization</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<p style='text-align:center;color:gray;'>"
    "Bubble size represents the primary parameter. "
    "Bubble color represents the secondary parameter."
    "</p>",
    unsafe_allow_html=True
)

st.divider()

if plot:

    plot_df = df if selected_state == "Overall India" else df[df["State"] == selected_state]
    zoom_level = 4 if selected_state == "Overall India" else 5.5

    fig = px.scatter_mapbox(
        plot_df,
        lat="Latitude",
        lon="Longitude",
        size=primary,
        color=secondary,
        hover_name="District",
        zoom=zoom_level,
        mapbox_style=map_style,
        size_max=bubble_multiplier * 8,
        color_continuous_scale=color_scale,
        height=700
    )

    fig.update_layout(
        showlegend=show_legend,
        coloraxis_showscale=show_legend,
        margin=dict(l=0, r=0, t=0, b=0)
    )

    st.plotly_chart(fig, use_container_width=True)

else:
    st.info("Select parameters from the sidebar and click Plot Map.")
