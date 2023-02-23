import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import make_interp_spline


def show_all_airspace_layers(_airspace_types, ahn, graph_width, graph_height):
    fig, ax = plt.subplots(figsize=(8, 6))
    colors = ['green', 'yellow', 'red', 'orange', 'blue', 'purple', 'black']
    colors_dict = {}
    for i, (key, value) in enumerate(_airspace_types.items()):
        x1, x2, ll, ul = value["x1"], value["x2"], value["ll"], value["ul"]
        if key in colors_dict:
            color = colors_dict[key]
        else:
            color = colors[len(colors_dict) % len(colors)]
            colors_dict[key] = color
        draw_airspace_layer(ax, x1, x2, ll, ul, color, key)
    draw_ground_elevation(ahn)
    ax.set_ylim([0, 2500])
    ax.set_xlim([0, 170])
    ax.legend()
    plt.show()


def draw_airspace_layer(ax, x1, x2, ll, ul, color, label):
    x = [x1, x2]
    ax.fill_between(x, ll, ul, facecolor=color, alpha=0.5, label=label)
    # Add a line for y1
    x_values = np.linspace(x1, x2, num=1000)
    y1_values = np.full_like(x_values, ll)
    ax.plot(x_values, y1_values, color=color, alpha=1, linestyle='dashed')
    # Add a line for y2
    y2_values = np.full_like(x_values, ul)
    ax.plot(x_values, y2_values, color=color, alpha=1, linestyle='dashed')
    # Add a label in the center of the plot
    x_center = (x1 + x2) / 2
    y_center = (ll + ul) / 2
    bbox_props = dict(facecolor='white', edgecolor=color, linewidth=1, alpha=0.9)
    ax.text(x_center, y_center, label, ha='center', va='center', weight='bold', bbox=bbox_props)


def draw_ground_elevation(ahn):
    # Extract x and y data from dictionary
    x_data = []
    y_data = []
    for step in ahn.values():
        x_data.append(step['x1'])
        y_data.append(step['height'])

    # Interpolate the data with a spline
    x_smooth = np.linspace(min(x_data), max(x_data), 300)
    y_spline = make_interp_spline(x_data, y_data)(x_smooth)

    # Plot the smoothed line
    plt.plot(x_smooth, y_spline)

    # Add axis labels and a title
    plt.xlabel('Distance (m)')
    plt.ylabel('Height (m)')
    plt.title('Height profile')

    # Show the plot
    plt.show()


