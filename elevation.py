import requests
import json
from pyproj import Transformer


def get_elevation(xmin, ymin, xmax, ymax):

    url = "https://service.pdok.nl/rws/ahn3/wms/v1_0"
    params = {
        "SERVICE": "WMS",
        "VERSION": "1.3.0",
        "REQUEST": "GetFeatureInfo",
        "FORMAT": "image/png",
        "TRANSPARENT": "true",
        "QUERY_LAYERS": "ahn3_5m_dtm",
        "LAYERS": "ahn3_5m_dtm",
        "INFO_FORMAT": "application/json",
        "I": "50",
        "J": "50",
        "CRS": "EPSG:28992",
        "STYLES": "",
        "WIDTH": "101",
        "HEIGHT": "101",
        "BBOX": f"{xmin},{ymin},{xmax},{ymax}"
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()
        print(data)
        value_list = data['features'][0]['properties']['value_list']

        return float(value_list)

    except Exception as e:

        return 'none'


def convert_utm(lat1, lon1):
    transformer = Transformer.from_crs("EPSG:4326", "EPSG:28992")
    lat2 = lat1 + 0.00000001
    lon2 = lon1 + 0.00000001
    x1, y1 = transformer.transform(lat1, lon1)
    x2, y2 = transformer.transform(lat2, lon2)
    xmin = min(x1, x2)
    xmax = max(x1, x2)
    ymin = min(y1, y2)
    ymax = max(y1, y2)

    try:
        return get_elevation(xmin, ymin, xmax, ymax)

    except Exception as e:
        print(f"An error occurred: {e}")

        return None
