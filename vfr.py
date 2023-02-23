import requests
import requests.packages.urllib3.exceptions
from urllib3.exceptions import InsecureRequestWarning

fttom = 0.3048
fltom = 100 * fttom


def get_layers(lat, lon, distance):
    # Disable SSL certificate verification
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

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
        "returnGeometry": "false",
        "maxAllowableOffset": "",
        "geometryPrecision": "",
        "dynamicLayers": "",
        "mapExtent": f"{lon - 0.01},{lat - 0.01},{lon + 0.01},{lat + 0.01}",
        "mapScale": "",
        "f": "pjson"
    }

    # Send a GET request to the REST endpoint and parse the response
    response = requests.get(url, params=params, verify=False)
    data = response.json()

    # Strip the data and put it every layer in airspaces
    layers = len(data["results"])
    airspaces = {}
    for i in range(layers):
        layer = data["results"][i]["attributes"]
        ull = layer["UOM Lower Limit"]
        uul = layer["UOM Upper Limit"]
        rll = layer["Reference Lower Limit"]
        rul = layer["Reference Upper Limit"]
        if layer["Airspace Type"] == 'CLASS' and layer['Airspace Class'] == 'E':
            if uul == 'FT':
                ll = round(float(layer["Upper Limit"]) * fttom)
            else:
                ll = round(float(layer["Upper Limit"]) * fltom)
            ul = ll
        else:
            if layer["Local Type Designator"] == 'PJA':
                if ull == 'FT':
                    ll = round(float(layer["Lower Limit"]) * fttom)
                else:
                    ll = round(float(layer["Lower Limit"]) * fltom)
                if uul == 'FT':
                    ul = round(float(layer["Upper Limit"]) * fttom)
                else:
                    ul = round(float(layer["Upper Limit"]) * fltom)
            else:
                if layer["Airspace Type"] == "TMA":
                    if ull == 'FT':
                        ll = round(float(layer["Lower Limit"]) * fttom)
                    else:
                        ll = round(float(layer["Lower Limit"]) * fltom)
                    if uul == 'FT':
                        ul = round(float(layer["Upper Limit"]) * fttom)
                    else:
                        ul = round(float(layer["Upper Limit"]) * fltom)
                else:
                    continue

        airspaces[layer["Airspace Name"]] = {
            "ll": ll,
            "ul": ul,
            "distance": distance,
            "rll": rll,
            "rul": rul,
        }

    return airspaces
