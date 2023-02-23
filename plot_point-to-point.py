import elevation
import flightpath
import airspace_plotter
import vfr

# locations to choose
E = (51.56667, 4.93333, 'EHGR')
H = (52.72917, 6.51667, 'HOOGEVEEN')
V = (51.363650, 6.218165, 'VENLO')
M = (51.12682342529297, 5.947177886962891, 'MONTFORT')

# starting and ending point and the distance in km between every datapoint
A = E
B = H
gap = 5

# size of the graph
graph_height = 2100


print(f"route from {A} to {B} with datapoint every {gap}km")

# getting the datapoints back in lat, lon for horizontal steps
points = flightpath.generate_route_by_gap(A[0], A[1], B[0], B[1], gap)

# counting the horizontal steps points for iterations
steps = len(points)

# getting the layer attributes per horizontal step
layer_dict = {}
ahn_dict = {}
for i in range(steps):
    distance = 0
    lat = points[f"step" + str(i + 1)]["lat"]
    lon = points[f"step" + str(i + 1)]["lon"]
    layer = vfr.get_layers(lat, lon, distance)
    ahn = elevation.convert_utm(lat, lon)
    for key in layer:
        layer[key]["x1"] = i * gap
        layer[key]["x2"] = i * gap + gap
    print(f"step {i} {layer}")
    layer_dict[f"step{i + 1}"] = layer
    ahn_dict[f"step{i + 1}"] = {
        "x1": i * gap,
        "x2": i * gap + gap,
        "height": ahn,
    }

# do something to form a dictionary like airspace_types
graph_width = steps * gap
simon = {}
for step in layer_dict:
    for key, value in layer_dict[step].items():
        if key not in simon:
            simon[key] = value
        else:
            simon[key]['x2'] = value['x2']

# get the plots for every airspace_layer and print them
airspace_plotter.show_all_airspace_layers(simon, ahn_dict, graph_width, graph_height)
