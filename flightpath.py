from haversine import haversine, Unit
from variables import A, B, gap, gl_resolution
import elevation
import vfr


def generate_datapoints_by_delta(lat1, lon1, lat2, lon2, delta):
    # Calculate the distance between the two geolocations
    distance = haversine((lat1, lon1), (lat2, lon2), unit=Unit.KILOMETERS)

    # Calculate the number of points to generate
    num_points = int(distance / delta)

    # Generate the points
    lat_step = (lat2 - lat1) / num_points
    lon_step = (lon2 - lon1) / num_points

    # Store the lat/lon data in a list
    route = []
    for i in range(num_points):
        lat = lat1 + (i * lat_step)
        lon = lon1 + (i * lon_step)
        point = (lat, lon)
        route.append(point)
    print(f" - finished generate_datapoints_by delta: {route}\n")
    return route


def calculate_distance(lat1, lon1, lat2, lon2):
    # Calculate the distance between the two geolocations
    distance = haversine((lat1, lon1), (lat2, lon2), unit=Unit.METERS)

    return distance


def transform_coordinates(lat, lon, height):
    lat_deg = float(lat[:2])  # degrees
    lat_min = float(lat[2:4] + '.' + lat[4:7])  # minutes
    lon_deg = float(lon[0])  # degrees
    lon_min = float(lon[1:3] + '.' + lon[3:6])  # minutes
    lat_dd = round(lat_deg + (lat_min / 60), 5)  # decimal degrees
    lon_dd = round(lon_deg + (lon_min / 60), 5)  # decimal degrees

    return lat_dd, lon_dd, height


def read_igc_file(filepath):
    with open(filepath, 'r') as f:
        igc_lines = f.readlines()

    # Skip all lines until the first B record
    b_records_start_index = next(i for i, line in enumerate(igc_lines) if line.startswith('B'))

    # Extract the B records and convert them to tuples with lat, lon, and alt
    b_records = igc_lines[b_records_start_index:]

    tulips = []
    for record in b_records:
        lat = record[7:15]
        lon = record[17:24]
        height = int(record[31:35])
        tulips.append(transform_coordinates(lat, lon, height))

    return tulips


def get_airspace_layers():
    datapoints = generate_datapoints_by_delta(A[0], A[1], B[0], B[1], gap)
    steps_layers = len(datapoints)
    graph_width = steps_layers * gap
    airspace_layers = {}
    for i in range(steps_layers):
        layer = vfr.get_layers(datapoints[i][0], datapoints[i][1])
        for o in range(len(layer)):
            layer[o]["x1"] = i * gap
            layer[o]["x2"] = i * gap + gap
            if layer[o]["Airspace Ident"] in airspace_layers:
                airspace_layers[layer[o]["Airspace Ident"]]["x2"] = layer[o]["x2"]
            else:
                airspace_layers[layer[o]["Airspace Ident"]] = layer[o]

    return airspace_layers, graph_width


def get_ground_elevation():
    datapoints = generate_datapoints_by_delta(A[0], A[1], B[0], B[1], gl_resolution)
    # counting the horizontal steps points for iterations
    steps_gl = len(datapoints)

    # getting the elevation per horizontal step
    ahn_dict = {}

    for i in range(steps_gl):
        ahn = elevation.convert_utm(datapoints[i][0], datapoints[i][1])
        ahn_dict[f"step{i + 1}"] = {
            "x1": i * gl_resolution,
            "x2": i * gl_resolution + gl_resolution,
            "height": ahn,
        }

    return ahn_dict

