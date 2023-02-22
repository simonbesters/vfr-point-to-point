import matplotlib.pyplot as plt
import numpy as np


def get_all_airspace_layers(_airspace_types):
    fig, ax = plt.subplots(figsize=(8, 6))
    colors = ['green', 'yellow', 'red', 'orange', 'blue', 'purple', 'black']
    colors_dict = {}
    for i, (key, value) in enumerate(_airspace_types.items()):
        x1, x2, y1, y2 = value["x1"], value["x2"], value["y1"], value["y2"]
        if key in colors_dict:
            color = colors_dict[key]
        else:
            color = colors[len(colors_dict) % len(colors)]
            colors_dict[key] = color
        draw_airspace_layer(ax, x1, x2, y1, y2, color, key)
    ax.set_ylim([0, 2500])
    ax.set_xlim([0, 170])
    ax.legend()
    plt.show()


def draw_airspace_layer(ax, x1, x2, y1, y2, color, label):
    x = [x1, x2]
    ax.fill_between(x, y1, y2, facecolor=color, alpha=0.5, label=label)
    # Add a line for y1
    x_values = np.linspace(x1, x2, num=1000)
    y1_values = np.full_like(x_values, y1)
    ax.plot(x_values, y1_values, color=color, alpha=1, linestyle='dashed')
    # Add a line for y2
    y2_values = np.full_like(x_values, y2)
    ax.plot(x_values, y2_values, color=color, alpha=1, linestyle='dashed')
    # Add a label in the center of the plot
    x_center = (x1 + x2) / 2
    y_center = (y1 + y2) / 2
    bbox_props = dict(facecolor='white', edgecolor=color, linewidth=1, alpha=0.9)
    ax.text(x_center, y_center, label, ha='center', va='center', weight='bold', bbox=bbox_props)





