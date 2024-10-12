import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import matplotlib.colors as mcolors
import qwerty_layout
import random
def gradual_decay(distance, radius):
    return (1 - (distance / radius) ** 3) * (distance <= radius)


def genKeyboardLayout(ax: plt.axes, layout: dict):
    """this function takes in an Axes object, and a layout,
    and generates the keyboard layout in matplotlib figure
    It ignores space, ctrl, alt as they are not required in the heatmap
    generation
    """

    for key in layout:

        pos = layout[key]["pos"]  # position tuple (x,y)
        if key[:5] == "Shift":  # special case for shift for longer length rectangeles
            rect = Rectangle(
                pos, 2.25, 1, edgecolor="black", linewidth=1, facecolor="none"
            )  # adds the rectangle, and the text in the middle
            ax.text(
                pos[0] + 1,
                pos[1] + 0.5,
                key,
                ha="center",
                va="center",
                color="black",
            )

        elif key not in [
            "Ctrl_L",
            "Alt_L",
            "Space",
            "Alt_R",
            "Ctrl_R",
        ]:  # ignoring the bottom row, not relevant for heatmap generation
            rect = Rectangle(
                pos, 1, 1, edgecolor="black", linewidth=1, facecolor="none"
            )  # adds the rectangle, and the text in the middle
            ax.text(
                pos[0] + 0.5,
                pos[1] + 0.5,
                key,
                ha="center",
                va="center",
                color="black",
            )
        ax.add_patch(rect)


def genFreq(inpStr: str, layout, characters: dict) -> tuple[np.array, np.array]:
    """
    This function takes in an input string, the layout dictionary, and the characters dictionary,
    returns 2 lists, one containing x coordinates of all the key presses, y coordinates of all the key presses
    """
    x, y = list(), list()

    for char in inpStr:
        keys = characters[char]
        for key in keys:  # for each key to be pressed
            if key == "Space":  # we need to ignore space, as it skews the heatmap
                continue
            # adding offset to pad to center
            x.append(layout[key]["pos"][0] + 0.5)
            y.append(layout[key]["pos"][1] + 0.5)

    return x, y



def plot1(
    x: np.array,
    y: np.array,
    grid_size: tuple,
):
    """
    Function generates plot without animation
    """
    # heatmap matrix, and grid limits
    heatmap = np.zeros(grid_size)
    x_min, x_max = 0, 14.5
    y_min, y_max = 1, 5

    # generates grid for heatmap
    x_grid = np.linspace(x_min, x_max, grid_size[0])
    y_grid = np.linspace(y_min, y_max, grid_size[1])
    X, Y = np.meshgrid(x_grid, y_grid, indexing="xy")
    radius = 0.6

    for i in range(len(x)):
        # Calculate the distance from each grid point to the (x[i], y[i]) point
        distance = np.sqrt((X - x[i]) ** 2 + (Y - y[i]) ** 2).T

        # Add to the heatmap within the circular region
        influence = 1 * (distance <= radius) * gradual_decay(distance, radius)

        heatmap += influence

    # generating colormaps
    colors = ["blue", "green", "yellow", "orange", "red"]
    blue_red = mcolors.LinearSegmentedColormap.from_list("blue_red", colors)

    plt.imshow(
        heatmap.T,
        cmap=blue_red,
        interpolation="gaussian",
        extent=[x_min, x_max, y_min, y_max],
        origin="lower",
        alpha=0.4,
    )
    # Save the plot
    plt.savefig("heatmap.png")


def caculate_key_travel(input_string: str, layout: dict, keys: dict):
    """
    This function calculates the key travel, taking in the input string, the layout
    dictionary and the keys dictionary
    """
    sum = 0
    for c in input_string:
        for key in keys[c]:  # iterating for each key to be pressed
            if key == "Space": #ignoring space  
                continue
            start_key = layout[key]["start"]  # home row key to be used
            pos1 = layout[start_key]["pos"]
            pos2 = layout[key]["pos"]
            distance = np.sqrt((pos2[1] - pos1[1]) ** 2 + (pos2[0] - pos1[0]) ** 2)
            sum += distance
    return sum

def neighbour_solution(keys:dict) -> dict:
    new_keys = keys.copy()
    i, j = random.sample(range(len(keys)),2)
    #only keys themselves change, not pos or homerow key
    new_keys[i], new_keys[j] = new_keys[j], new_keys[i] 

if __name__ == "__main__":

    fig, ax = plt.subplots(figsize=(14, 8))  # generating axes , fig object
    # setting limits for axes
    ax.set_xlim(-2, 16)
    ax.set_ylim(-1, 6)
    ax.set_aspect("equal")
    ax.axis("off")
    layout = qwerty_layout
    # generating thhe keyboard layout
    genKeyboardLayout(ax, layout.keys)

    grid_size = (58, 16)  # Number of pixels in x and y`

    inputStr = input("Enter string : ")
    x, y = genFreq(
        inputStr, layout.keys, layout.characters
    )  # x coordinate and y coordinates of each keypress
    distance = caculate_key_travel(
        inputStr, layout.keys, layout.characters
    )  # calculating the key travel disance




    print(f"Total distance travelled is {distance} units")
