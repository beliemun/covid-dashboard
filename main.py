import dash
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd
from data import countries_df, totals_df
from builder import make_table

stylesheets = [
    "https://cdn.jsdelivr.net/npm/reset-css@5.0.1/reset.min.css",
    "https://fonts.googleapis.com/css2?family=Open+Sans&display=swap",
]

bars_graph = px.bar(
    totals_df,
    x="condition",
    y="count",
    template="plotly_dark",
    title="Total Golbal Cases",
    hover_data={"count": ":,"},
    labels={"condition": "Condition", "count": "Count"},
    # color=["Confirmed", "Deaths", "Recovered"],
)
bars_graph.update_traces(marker_color=["#e74c3c", "#9b59b6", "#2ecc71"])

app = dash.Dash(__name__, external_stylesheets=stylesheets)

buble_map = px.scatter_geo(
    countries_df,
    locations="Country_Region",
    locationmode="country names",
    color="Confirmed",
    color_continuous_scale=px.colors.sequential.Oryel,
    hover_name="Country_Region",
    hover_data={
        "Country_Region": False,
        "Confirmed": ":,.0f",
        "Recovered": ":,.0f",
        "Deaths": ":,.0f",
    },
    size="Confirmed",
    size_max=50,
    title="Confirmed By Country",
    template="plotly_dark",
    projection="natural earth",
    height=600,
)
buble_map.update_layout(margin=dict(l=0, t=50, r=0, b=30))

grid_style = {
    "display": "grid",
    "gridTemplateColumns": "repeat(6, 1fr)",
    "gap": "20px",
}
app.layout = html.Div(
    style={
        "minHeight": "100vh",
        "backgroundColor": "#222222",
        "color": "white",
    },
    children=[
        html.Header(
            style={"textAlign": "center", "paddingTop": "50px"},
            children=[
                html.H1(
                    "Corona Dashboard",
                    style={
                        "fontSize": "50px",
                        "fontFamily": "Open Sans, sans-serif",
                        "marginBottom": "30px",
                    },
                )
            ],
        ),
        html.Div(
            style=grid_style,
            children=[
                html.Div(
                    style={
                        "gridColumn": "span 4",
                    },
                    children=[dcc.Graph(figure=buble_map)],
                ),
                html.Div(
                    style={
                        "gridColumn": "span 2",
                        "height": "600px",
                        "overflow-y": "auto",
                        "overflow-x": "hidden",
                    },
                    children=[make_table(countries_df)],
                ),
                html.Div(
                    style={"gridColumn": "span 1"},
                    children=[dcc.Graph(figure=bars_graph)],
                ),
            ],
        ),
    ],
)

if __name__ == "__main__":
    app.run_server(debug=True)
