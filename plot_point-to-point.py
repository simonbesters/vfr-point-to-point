import flightpath
import airspace_plotter
from variables import A, B, graph_height, gap

print(f"\nSTART: route from {A} to {B} with datapoint every {gap}km \n")

# get airspace types
print("1. start get_airspace_layers \n")
airspace_layers, graph_width = flightpath.get_airspace_layers()
print("2. finish get_airspace_layers \n")

# get ground level elevation
print("3. start get_ground_elevation \n")
ground_level_elevation = flightpath.get_ground_elevation()
print("4. finish get_ground_elevation \n")

# construct graph
print("5. start construct_graph \n")
ax = airspace_plotter.construct_graph(graph_width, graph_height)
print("6. finish construct_graph \n")

# draw ground level elevation
print("7. start draw_ground_elevation \n")
airspace_plotter.draw_ground_elevation(ground_level_elevation)
print("8. finish draw_ground_elevation \n")

# draw airspace layers
print("9. start construct_airspace \n")
airspace_plotter.construct_airspace(airspace_layers, ax)
print("10. finish construct_airspace \n")

# show graph
print("11. start show_graph \n")
airspace_plotter.show_graph()
print("12. finish show_graph \n")
