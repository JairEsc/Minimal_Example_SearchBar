import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import dash_leaflet as dl
import json
from dash import ctx

# Sample GeoJSON data with two polygons
geojson_data = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [-100.0, 40.0],
                        [-101.0, 40.0],
                        [-101.0, 41.0],
                        [-100.0, 41.0],
                        [-100.0, 40.0]
                    ]
                ]
            },
            "properties": {
                "name": "Polygon 1",
                "popup": "This is Polygon 1"
            }
        },
        {
            "type": "Feature",
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [-102.0, 42.0],
                        [-103.0, 42.0],
                        [-103.0, 43.0],
                        [-102.0, 43.0],
                        [-102.0, 42.0]
                    ]
                ]
            },
            "properties": {
                "name": "Polygon 2",
                "popup": "This is Polygon 2"
            }
        }
    ]
}

# Save GeoJSON to a file (optional, for demonstration purposes)
with open("polygons.geojson", "w") as f:
    json.dump(geojson_data, f)

# Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Dash App with GeoJSON Polygons"),
    dcc.Dropdown(
        id="polygon-dropdown",
        options=[
            {"label": "Polygon 1", "value": "Polygon 1"},
            {"label": "Polygon 2", "value": "Polygon 2"}
        ],
        placeholder="Select a polygon"
    ),
    dl.Map(center=[41.0, -101.0], zoom=5, children=[
        dl.TileLayer(),
        dl.GeoJSON(data=geojson_data, id="geojson")
    ], style={'width': '100%', 'height': '500px'}, id="map")
])

@app.callback(
    Output("geojson", "clickData"),
    Input("polygon-dropdown", "value"),
    prevent_initial_call=True
)
def update_click_data_from_dropdown(selected_polygon):
    if not selected_polygon:
        return dash.no_update
    # Find the feature corresponding to the selected polygon
    for feature in geojson_data["features"]:
        if feature["properties"]["name"] == selected_polygon:
            return {"geometry": feature["geometry"]}
    return dash.no_update

@app.callback(
    Output("map", "viewport"),
    Input("geojson", "clickData"),
    prevent_initial_call=True
)
def update_viewport_on_click(feature):
    if not feature:
        return {"center": [41.0, -101.0], "zoom": 6}  # Default center and zoom
    # Get the center of the clicked polygon
    coords = feature["geometry"]["coordinates"][0]
    lat = sum(coord[1] for coord in coords) / len(coords)
    lon = sum(coord[0] for coord in coords) / len(coords)
    return {"center": [lat, lon], "zoom": 12}  # Zoom level 12 for a closer view

# @app.callback(
#     Output("map", "viewport"),
#     Input("map", "zoom"),State("map", "center"),prevent_initial_call=True
# )
# def update_viewport_on_zoom(zoom,center):
#     # Default center remains the same, only zoom level changes
#     return {"center": center, "zoom": zoom}

if __name__ == "__main__":
    app.run(debug=True)