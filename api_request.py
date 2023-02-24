import urllib3
import json

lat = 51.56667
lon = 4.93333

urllib3.disable_warnings()

http = urllib3.PoolManager(
    num_pools=10,  # number of connection pools to create
    maxsize=10,  # maximum number of connections to keep in each pool
    block=True,  # whether to block when all connections in a pool are in use
    timeout=30,  # connection timeout in seconds
    retries=3,  # whether to retry failed requests
    headers=None,  # default headers to include with each request
    cert_reqs='CERT_NONE'  # SSL certificate verification disabled
)

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


def datapoint_request():
    response = None
    try:
        response = http.request('GET', url, fields=params)
    except Exception as e:
        print(f"Error scraping URL: {url}. Exception: {e}")
    finally:
        if response is not None:
            response.release_conn()
    json_data = json.loads(response.data.decode('utf-8'))
    print(json_data)


datapoint_request()

