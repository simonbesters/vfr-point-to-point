import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning


def getLayers(lat, lon):
    # Disable SSL certificate verification
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

    # Set the geolocation of interest (latitude and longitude)
    # lat, lon = 51.56667, 4.93333  # Gilze-Rijen coordinates

    # Set the REST endpoint URL and parameters for the identify operation
    url = "https://geoservices.lvnl.nl/arcgis/rest/services/VFRchart/Airspaces/MapServer/identify/"
    params = {
        "geometryType": "esriGeometryPoint",
        "geometry": f"{lon},{lat}",
        "tolerance": 5,
        "layers": "all",
        "layerDefs": "",
        "time": "",
        "layerTimeOptions": "",
        "imageDisplay": "500,500,96",
        "returnGeometry": "true",
        "maxAllowableOffset": "",
        "geometryPrecision": "",
        "dynamicLayers": "",
        "mapExtent": f"{lon-0.01},{lat-0.01},{lon+0.01},{lat+0.01}",
        "mapScale": "",
        "f": "pjson"
    }

    # Send a GET request to the REST endpoint and parse the response
    response = requests.get(url, params=params, verify=False)
    data = response.json()
    layers = len(data["results"])
    airspaces = {}
    for i in range(layers):
        layer = data["results"][i]["attributes"]
        unit1 = layer["UOM Lower Limit"]
        unit2 = layer["UOM Upper Limit"]
        if unit1 == 'FT':
            y1 = round(float(layer["Lower Limit"]) * 0.3048)
        else:
            y1 = round(float(layer["Lower Limit"]) * 0.3048 * 100)
        if unit2 == 'FT':
            y2 = round(float(layer["Upper Limit"]) * 0.3048)
        else:
            y2 = round(float(layer["Upper Limit"]) * 0.3048 * 100)
        if y2 >= maxheight:
            continue
        airspaces[layer["Airspace Name"]] = {
            "y1": y1,
            "y2": y2,
        }

    return airspaces
