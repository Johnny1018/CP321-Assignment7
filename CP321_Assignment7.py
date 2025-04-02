import pandas as pd
import dash
from dash import dcc, html, Input, Output
import plotly.express as px

# Load dataset
df = pd.read_csv("world_cup_finals.csv")

# Normalize for mapping but keep original names for UI
df["Map_Winners"] = df["Winners"].replace({
    "West Germany": "Germany",
    "England": "United Kingdom"
})
df["Map_RunnersUp"] = df["Runners-up"].replace({
    "West Germany": "Germany",
    "England": "United Kingdom"
})

# Count wins using mapped winners
win_counts = df["Map_Winners"].value_counts().reset_index()
win_counts.columns = ["Country", "Wins"]

# Initialize Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("FIFA World Cup Dashboard", style={'textAlign': 'center'}),

    dcc.Graph(id="choropleth-map"),

    html.Label("Select a Country:"),
    dcc.Dropdown(
        id="country-dropdown",
        options=[{"label": c, "value": c} for c in sorted(df["Winners"].unique())],
        placeholder="Select a country"
    ),
    html.Div(id="win-output", style={"marginBottom": "20px"}),

    html.Label("Select a Year:"),
    dcc.Dropdown(
        id="year-dropdown",
        options=[{"label": y, "value": y} for y in sorted(df["Year"].unique())],
        placeholder="Select a year"
    ),
    html.Div(id="final-output")
])

@app.callback(
    Output("choropleth-map", "figure"),
    Input("country-dropdown", "value")
)
def update_map(selected_country):
    fig = px.choropleth(
        win_counts,
        locations="Country",
        locationmode="country names",
        color="Wins",
        color_continuous_scale="Reds",
        title="World Cup Wins by Country",
        scope="world"
    )

    fig.update_geos(
        showcountries=True,
        showcoastlines=True,
        showland=True,
        fitbounds="locations",
        projection_type="natural earth"
    )

    fig.update_layout(
        margin={"r": 0, "t": 40, "l": 0, "b": 0},
        height=600,
    )
    
    return fig

@app.callback(
    Output("win-output", "children"),
    Input("country-dropdown", "value")
)
def display_country_wins(country):
    if not country:
        return ""
    count = df[df["Winners"] == country].shape[0]
    return f"{country} has won the World Cup {count} time(s)."

@app.callback(
    Output("final-output", "children"),
    Input("year-dropdown", "value")
)
def display_final(year):
    if not year:
        return ""
    row = df[df["Year"] == year].iloc[0]
    return f"In {year}, the winner was {row['Winners']} and the runner-up was {row['Runners-up']}."

if __name__ == "__main__":
    import os
    
    port = int(os.environ.get("PORT", 8050))
    app.run(host="0.0.0.0", port=port)
