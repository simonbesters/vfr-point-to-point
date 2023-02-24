import requests
import requests.packages.urllib3.exceptions
from urllib3.exceptions import InsecureRequestWarning
from variables import feet_to_meters, flightlevel_to_meters


def get_layers(lat, lon):
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
    airspaces = []
    for i in range(layers):
        layer = data["results"][i]["attributes"]
        if layer["Airspace Type"] == 'CLASS' and layer["Airspace Class"] == 'E' or \
                layer["Local Type Designator"] == 'PJA' or layer["Airspace Type"] == "TMA":
            lower_limit_meters = round(
                float(layer["Lower Limit"]) *
                (feet_to_meters if layer["UOM Lower Limit"] == 'FT' else flightlevel_to_meters))
            upper_limit_meters = round(
                float(layer["Upper Limit"]) *
                (feet_to_meters if layer["UOM Upper Limit"] == 'FT' else flightlevel_to_meters))
        else:
            continue

        new_layer = {
            "Airspace Ident": layer["Airspace Ident"],
            "Airspace Name": layer["Airspace Name"],
            "Airspace Type": layer["Airspace Type"],
            "Airspace Class": layer["Airspace Class"],
            "Local Type Designator": layer["Local Type Designator"],
            "Lower Limit": lower_limit_meters,
            "Upper Limit": upper_limit_meters,
            "Reference_ll": layer["Reference Lower Limit"],
            "Reference_ul": layer["Reference Upper Limit"],
        }

        airspaces.append(new_layer)

    return airspaces
