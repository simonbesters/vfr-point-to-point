import airspace_plotter
import vfr
import flightpath
import matplotlib.pyplot as plt

points = flightpath.read_igc_file('input/293XZAP30.igc')

# counting the horizontal steps points for iterations
steps = len(points)

lat, lon, height = zip(*points)

data = []
x2 = 0
for i in range(steps - 1):
    x1 = x2
    lat1 = lat[i]
    lon1 = lon[i]
    lat2 = lat[1 + i]
    lon2 = lon[1 + i]
    height2 = height[1 + i]
    distance = flightpath.calculate_distance(lat1, lon1, lat2, lon2)
    x3 = x2 + distance
    x2 = x3

    data.append((lat2, lon2, x1, x2, distance, height2))

# Extract x and y data from tuples
x_data = []
y_data = []

for i in range(len(data)):
    x_data.append(data[i][2])
    y_data.append(data[i][5])

# plot > move backward
plt.plot(x_data, y_data)
plt.xlabel('Distance (m)')
plt.ylabel('Height (m)')
plt.show()

# getting the layer attributes per horizontal step
layer_dict = {}
for i in range(steps):
    lat = data[i][0]
    lon = data[i][1]
    distance = data[i][2]
    print(distance)
    layer = vfr.get_layers(lat, lon, distance)
    print(layer)
    for key in layer:
        if key == 0:
            continue
        else:
            y1 = layer[key]["y1"]
            y2 = layer[key]["y2"]
            layer[key] = {
                "y1": layer[key]["y1"],
                "y2": layer[key]["y2"],
                "x1": layer[key]["distance"],
                "x2": layer[key]["x1"]
            }
    print(f"step {i} {layer}")
    layer_dict[f"step{i + 1}"] = layer

print(f"layerdict{layer_dict}")
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
airspace_plotter.show_all_airspace_layers(simon)
