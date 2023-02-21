import route
import airspace_plotter
import vfr_layer_getter

# starting and ending point and the distance in km between every datapoint
A = (51.56667, 4.93333, 'EHGR')
B = (52.72917, 6.51667, 'HOOGEVEEN')
gap = 5

print(f"route from {A} to {B} with datapoint every {gap}km")

# getting the datapoints back in lat, lon for horizontal steps
points = route.generate_route(A[0], A[1], B[0], B[1], gap)

# counting the horizontal steps points for iterations
steps = len(points)

# getting the layer attributes per horizontal step
layer_dict = {}
for i in range(steps):

    lat = points[f"step" + str(i + 1)]["lat"]
    lon = points[f"step" + str(i + 1)]["lon"]
    # layer = vfr_layer_getter.getLayers(lat, lon)[i]["attributes"]
    layer = vfr_layer_getter.getLayers(lat, lon)
    for key in layer:
        layer[key]["x1"] = i * gap
        layer[key]["x2"] = i * gap + gap
    print(f"step {i} {layer}")
    layer_dict[f"step{i+1}"] = layer

print(layer_dict)
# do something to form a dictionary like airspace_types

simon = {}
for step in layer_dict:
    for key, value in layer_dict[step].items():
        if key not in simon:
            simon[key] = value
        else:
            simon[key]['x2'] = value['x2']

print(simon)


# get the plots for every airspace_layer and print them
airspace_plotter.get_all_airspace_layers(simon)

