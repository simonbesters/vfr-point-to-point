import math


def generate_route(lat1, lon1, lat2, lon2, gap):
    # Calculate the distance between the two geolocations
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c

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
