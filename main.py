import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
from data import (
    countries_df,
    make_global_df,
    make_country_df,
    totals_df,
    dropdown_options,
)
from builder import make_table

stylesheets = [
    "https://cdn.jsdelivr.net/npm/reset-css@5.0.1/reset.min.css",
    "https://fonts.googleapis.com/css2?family=Open+Sans&display=swap",
]
app = dash.Dash(__name__, external_stylesheets=stylesheets)

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
                        "gridRow": "span 2",
                        "height": "85vh",
                        "overflow-y": "auto",
                        "overflow-x": "hidden",
                    },
                    children=[make_table(countries_df)],
                ),
                html.Div(
                    style={"gridColumn": "span 1"},
                    children=[dcc.Graph(figure=bars_graph)],
                ),
                html.Div(
                    style={"gridColumn": "span 3"},
                    children=[
                        dcc.Dropdown(
                            id="country-input",
                            options=[
                                {"label": country, "value": country}
                                for country in dropdown_options
                            ],
                            style={
                                "width": 400,
                                "margin": "0 auto",
                                "color": "#222222",
                                "marginBottom": "15px",
                            },
                        ),
                        dcc.Graph(
                            id="country_graph",
                            style={"height": "400px"},
                        ),
                    ],
                ),
            ],
        ),
    ],
)


@app.callback(Output("country_graph", "figure"), [Input("country-input", "value")])
def update_hello(value):
    if value:
        df = make_country_df(value)
    else:
        df = make_global_df()
    fig = px.line(
        df,
        x="date",
        y=["confirmed", "deaths", "recovered"],
        template="plotly_dark",
        labels={
            "variable": "Condition",
            "date": "Date",
            "value": "Cases",
        },
        hover_data={
            "variable": False,
            "value": ":,",
        },
    )
    fig.update_xaxes(rangeslider_visible=True)
    return fig


if __name__ == "__main__":
    app.run_server(debug=True)
