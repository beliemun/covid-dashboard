from dash import html
from pandas.io.formats import style


def make_table(df):
    return html.Table(
        style={
            "width": "100%",
            "cellspacing": "10px",
        },
        children=[
            html.Thead(
                children=[
                    html.Tr(
                        children=[
                            html.Th(
                                column_name.replace("_", " "),
                                style={
                                    "fontSize": "20px",
                                    "fontWeight": "bold",
                                    "padding": "15px 0",
                                },
                            )
                            for column_name in df.columns
                        ]
                    )
                ],
            ),
            html.Tbody(
                children=[
                    html.Tr(
                        style={"borderBottom": "1px solid #404040"},
                        children=[
                            html.Td(
                                value_column,
                                style={
                                    "width": "50px",
                                    "fontSize": "16px",
                                    "textAlign": "center",
                                    "padding": "5px",
                                },
                            )
                            for value_column in value
                        ],
                    )
                    for value in df.values
                ]
            ),
        ],
    )
