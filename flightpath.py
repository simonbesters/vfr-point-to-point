from haversine import haversine, Unit


def generate_route_by_gap(lat1, lon1, lat2, lon2, gap):
    # Calculate the distance between the two geolocations
    distance = haversine((lat1, lon1), (lat2, lon2), unit=Unit.KILOMETERS)

    # Calculate the number of points to generate
    num_points = int(distance / gap)

    # Generate the points
    lat_step = (lat2 - lat1) / num_points
    lon_step = (lon2 - lon1) / num_points

    # Store the lat/lon data in a dictionary
    route = {}
    for i in range(num_points):
        lat = lat1 + (i * lat_step)
        lon = lon1 + (i * lon_step)
        point = {"lat": lat, "lon": lon}
        route[f"step{i + 1}"] = point

    return route


def generate_route_by_distance(lat1, lon1, lat2, lon2):
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
