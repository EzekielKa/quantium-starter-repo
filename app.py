import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd

df = pd.read_csv("data/output.csv")
df.columns = df.columns.str.strip()
df["date"] = pd.to_datetime(df["date"].str.strip())
df["region"] = df["region"].str.strip()

df = df.groupby("date")["sales"].sum().reset_index()
df = df.sort_values("date")

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Pink Morsel Sales Visualiser"),
    dcc.Graph(
        id="sales-chart",
        figure=px.line(
            df,
            x="date",
            y="sales",
            title="Pink Morsel Sales Over Time",
            labels={"date": "Date", "sales": "Sales ($)"},
        ).add_vline(
            x=pd.Timestamp("2021-01-15").timestamp() * 1000,
            line_dash="dash",
            line_color="red",
            annotation_text="Price Increase (15 Jan 2021)",
        ),
    ),
])

if __name__ == "__main__":
    app.run(debug=True)
