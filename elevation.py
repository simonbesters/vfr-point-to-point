import requests
import json
from pyproj import Transformer


def get_elevation(xmin, ymin, xmax, ymax):
    url = f"https://service.pdok.nl/rws/ahn3/wms/v1_0?SERVICE=WMS&VERSION=1.3.0&REQUEST=GetFeatureInfo&FORMAT=image%2Fpng&TRANSPARENT=true&QUERY_LAYERS=ahn3_5m_dtm&LAYERS=ahn3_5m_dtm&INFO_FORMAT=application%2Fjson&I=50&J=50&CRS=EPSG%3A28992&STYLES=&WIDTH=101&HEIGHT=101&BBOX={xmin},{ymin},{xmax},{ymax}"
    response = requests.get(url)
    print(f"response: {response}")
    # parse response content into JSON
    data = json.loads(response.content)
    if len(data['features']) == 0:
        print('No elevation data found.')

        return 0

    value_list = data['features'][0]['properties']['value_list']
    elevation = float(value_list)

    return elevation


def convert_utm(lat1, lon1):
    # Define the coordinate reference systems
    # wgs84 = pyproj.CRS("EPSG:4326")  # WGS84 in decimal degrees
    # utm = pyproj.CRS("EPSG:28992")  # UTM Zone 31N
    transformer = Transformer.from_crs("EPSG:4326","EPSG:28992")
    lat2 = lat1 + 0.00000001
    lon2 = lon1 + 0.00000001
    # Convert the input coordinates to UTM
    x1, y1 = transformer.transform(lat1, lon1)
    x2, y2 = transformer.transform(lat2, lon2)

    # Calculate the bounding box
    xmin = min(x1, x2)
    xmax = max(x1, x2)
    ymin = min(y1, y2)
    ymax = max(y1, y2)

    # Get the elevation for both bounding boxes
    return get_elevation(xmin, ymin, xmax, ymax)
