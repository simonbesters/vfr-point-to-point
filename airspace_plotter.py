import matplotlib.pyplot as plt
import numpy as np


def get_all_airspace_layers(_airspace_types):
    fig, ax = plt.subplots()
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





