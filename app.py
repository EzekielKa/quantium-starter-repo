import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd

df = pd.read_csv("data/output.csv")
df.columns = df.columns.str.strip()
df["date"] = pd.to_datetime(df["date"].str.strip())
df["region"] = df["region"].str.strip()

app = dash.Dash(__name__)

app.layout = html.Div(
    style={
        "fontFamily": "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
        "maxWidth": "900px",
        "margin": "40px auto",
        "padding": "30px",
        "backgroundColor": "#f8f9fa",
        "borderRadius": "12px",
        "boxShadow": "0 4px 20px rgba(0, 0, 0, 0.1)",
    },
    children=[
        html.H1(
            "Pink Morsel Sales Visualiser",
            style={
                "textAlign": "center",
                "color": "#d63384",
                "marginBottom": "5px",
                "fontSize": "28px",
            },
        ),
        html.P(
            "Filter by region to explore sales trends",
            style={
                "textAlign": "center",
                "color": "#6c757d",
                "marginBottom": "25px",
                "fontSize": "14px",
            },
        ),
        html.Div(
            style={
                "backgroundColor": "#fff",
                "padding": "15px 25px",
                "borderRadius": "8px",
                "marginBottom": "20px",
                "border": "1px solid #e9ecef",
            },
            children=[
                html.Label(
                    "Region",
                    style={
                        "fontWeight": "bold",
                        "color": "#495057",
                        "marginRight": "15px",
                        "fontSize": "14px",
                    },
                ),
                dcc.RadioItems(
                    id="region-filter",
                    options=[
                        {"label": " North", "value": "north"},
                        {"label": " East", "value": "east"},
                        {"label": " South", "value": "south"},
                        {"label": " West", "value": "west"},
                        {"label": " All", "value": "all"},
                    ],
                    value="all",
                    inline=True,
                    style={"display": "inline-block"},
                    inputStyle={"marginRight": "5px"},
                    labelStyle={
                        "marginRight": "20px",
                        "color": "#495057",
                        "fontSize": "14px",
                        "cursor": "pointer",
                    },
                ),
            ],
        ),
        html.Div(
            style={
                "backgroundColor": "#fff",
                "padding": "15px",
                "borderRadius": "8px",
                "border": "1px solid #e9ecef",
            },
            children=[
                dcc.Graph(id="sales-chart"),
            ],
        ),
    ],
)


@app.callback(
    Output("sales-chart", "figure"),
    Input("region-filter", "value"),
)
def update_chart(region):
    if region == "all":
        filtered = df.groupby("date")["sales"].sum().reset_index()
    else:
        filtered = (
            df[df["region"] == region]
            .groupby("date")["sales"]
            .sum()
            .reset_index()
        )
    filtered = filtered.sort_values("date")

    fig = px.line(
        filtered,
        x="date",
        y="sales",
        title="Pink Morsel Sales Over Time",
        labels={"date": "Date", "sales": "Sales ($)"},
    )
    fig.add_vline(
        x=pd.Timestamp("2021-01-15").timestamp() * 1000,
        line_dash="dash",
        line_color="red",
        annotation_text="Price Increase (15 Jan 2021)",
    )
    fig.update_layout(
        plot_bgcolor="#fff",
        paper_bgcolor="#fff",
        font_color="#495057",
        title_font_color="#d63384",
    )
    return fig


if __name__ == "__main__":
    app.run(debug=True)
