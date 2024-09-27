import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from collections import defaultdict
import matplotlib.colors as mcolors
import matplotlib.animation as animation
from matplotlib.image import AxesImage
import sys

def gradual_decay(distance, radius):
    return (1 - (distance / radius) ** 3) * (distance <= radius)

QWERTY_LAYOUT = {
    "row1": {
        "keys": "`1234567890-=",
        "positions": [
            (0, 0),
            (1, 0),
            (2, 0),
            (3, 0),
            (4, 0),
            (5, 0),
            (6, 0),
            (7, 0),
            (8, 0),
            (9, 0),
            (10, 0),
            (11, 0),
            (12, 0),
        ],
    },
    "row2": {
        "keys": "qwertyuiop[]\\",
        "positions": [
            (1.5, 1),
            (2.5, 1),
            (3.5, 1),
            (4.5, 1),
            (5.5, 1),
            (6.5, 1),
            (7.5, 1),
            (8.5, 1),
            (9.5, 1),
            (10.5, 1),
            (11.5, 1),
            (12.5, 1),
            (13.5, 1),
        ],
    },
    "row3": {
        "keys": "asdfghjkl;'",
        "positions": [
            (1.75, 2),
            (2.75, 2),
            (3.75, 2),
            (4.75, 2),
            (5.75, 2),
            (6.75, 2),
            (7.75, 2),
            (8.75, 2),
            (9.75, 2),
            (10.75, 2),
            (11.75, 2),
        ],
    },
    "row4": {
        "keys": "zxcvbnm,./",
        "positions": [
            (2.25, 3),
            (3.25, 3),
            (4.25, 3),
            (5.25, 3),
            (6.25, 3),
            (7.25, 3),
            (8.25, 3),
            (9.25, 3),
            (10.25, 3),
            (11.25, 3),
        ],
    },
    "special_keys": {
        "Shift_L": (0, 3),
        "Shift_R": (12.25, 3),
        "Space": (3.5, 4),
        "Backspace": (13, 0),
        "Tab": (0, 1),
        "CapsLock": (0, 2),
        "Enter": (12.75, 2),
    },
}


def smallest_greatest_elem(lst: list, x: float) -> float:
    """
    This function takes in a list and a float x,
    returns the smallest float that is greater than x
    """
    min = float("inf")
    for elem in lst:
        if elem > x and elem < min:
            min = elem
    return min


def genKeyboardLayout(ax: plt.axes, layout: dict) -> dict:
    special_keys = layout.pop("special_keys")
    cordinates = defaultdict(list)
    key_mapping = dict()
    # this dictionary stores the x values of every key at every y value
    # this comes in handy when we gen layout for special characters, and we need to determine their length
    for row in QWERTY_LAYOUT:
        for index, key in enumerate(QWERTY_LAYOUT[row]["keys"]):
            key_mapping[key] = QWERTY_LAYOUT[row]["positions"][index]
            pos = QWERTY_LAYOUT[row]["positions"][index]
            # Simulate a change in value based on the frame number
            cordinates[pos[1]].append(pos[0])
            rect = Rectangle(
                pos, 1, 1, edgecolor="black", linewidth=1, facecolor="none"
            )
            ax.add_patch(rect)
            ax.text(
                pos[0] + 0.5, pos[1] + 0.5, key, ha="center", va="center", color="black"
            )

    for specialkey in special_keys:
        pos = special_keys[specialkey]  # coordinates of the key
        key_mapping[specialkey] = special_keys[specialkey]
        length = (
            smallest_greatest_elem(cordinates[pos[1]], pos[0]) - pos[0]
        )  # length of the key
        if length > 3:
            length = 14.5 - pos[0]

        if specialkey == "Space":
            length = 6
        rect = Rectangle(
            pos, length, 1, edgecolor="black", linewidth=1, facecolor="none"
        )
        ax.add_patch(rect)
        ax.text(
            pos[0] + length / 2,
            pos[1] + 0.5,
            specialkey,
            ha="center",
            va="center",
            color="black",
        )
    return key_mapping


def genFreq(inpStr: str, keyMapping: dict) -> tuple[np.array, np.array, np.array]:
    x, y, z = list(), list(), list()

    for char in inpStr:
        try:
            coords = keyMapping[char]

            x.append(coords[0] + 0.5)
            y.append(coords[1] + 0.5)
            z.append(1)
        except:
            pass
    return x, y, z

def plot(inputStr:str, x:np.array, y:np.array, freq:np.array, gradualdecay, grid_size:tuple, ax, fig):
    heatmap = np.zeros(grid_size)
    x_min, x_max = 0,14.5
    y_min, y_max = 0,4

    x_grid = np.linspace(x_min, x_max, grid_size[0])
    y_grid = np.linspace(y_min, y_max, grid_size[1])
    X, Y = np.meshgrid(x_grid, y_grid, indexing="xy")
    radius = 0.6


    distance = np.sqrt((X - x[0]) ** 2 + (Y - y[0]) ** 2).T

    # Add the frequency to the heatmap within the circular region
    influence = (
        frequencies[0] * (distance <= radius) * gradual_decay(distance, radius)
    )

    heatmap += influence

    colors = ["blue", "green", "yellow", "orange", "red"]
    blue_red = mcolors.LinearSegmentedColormap.from_list("blue_red", colors)
    artist = ax.imshow(
            heatmap.T,
            cmap = blue_red,
            interpolation='gaussian',
            extent=[x_min, x_max, y_min, y_max],
            origin='lower',
            alpha=0.4
        )
    def update(frame):
        print(frame)
        nonlocal heatmap
        nonlocal artist
        artist.remove()
        i = frame
        distance = np.sqrt((X - x[i]) ** 2 + (Y - y[i]) ** 2).T

        # Add the frequency to the heatmap within the circular region
        influence = (
            frequencies[i] * (distance <= radius) * gradual_decay(distance, radius)
        )

        heatmap += influence
        artist = ax.imshow(
            heatmap.T,
            cmap = blue_red,
            interpolation='gaussian',
            extent=[x_min, x_max, y_min, y_max],
            origin='lower',
            alpha=0.4
        )
        return [artist]
    from matplotlib.animation import FuncAnimation
    ani = FuncAnimation(fig, update, frames=len(x), interval=0, blit=False, repeat=False)
    plt.show()
    #ani.save('animation.mp4', writer='ffmpeg', fps=60) 

def plot1(inputStr:str, x:np.array, y:np.array, freq:np.array, gradualdecay, grid_size:tuple):
    heatmap = np.zeros(grid_size)
    x_min, x_max = 0,14.5
    y_min, y_max = 0,4

    x_grid = np.linspace(x_min, x_max, grid_size[0])
    y_grid = np.linspace(y_min, y_max, grid_size[1])
    X, Y = np.meshgrid(x_grid, y_grid, indexing="xy")
    radius = 0.6

    for i in range(len(x)):
        # Calculate the distance from each grid point to the (x[i], y[i]) point
        distance = np.sqrt((X - x[i]) ** 2 + (Y - y[i]) ** 2).T

        # Add the frequency to the heatmap within the circular region
        influence = (
            frequencies[i] * (distance <= radius) * gradual_decay(distance, radius)
        )

        heatmap += influence
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
    plt.show()
    

def findkey(xcoords:list, input_key:str, keymapping:dict)->str:
    min_distance = 100
    ret_key = ''
    input_key = input_key.lower()
    for (xcoord, key) in xcoords:
        if abs(xcoord-keymapping[input_key][0]) <= min_distance:
            min_distance = abs(xcoord -keymapping[input_key][0])
            ret_key = key
    return ret_key

def caculate_key_travel(keymapping:dict , input_string:str, layout:dict):
    home_row_keys = {}
    # get the home row keys from row 3 (key 0-3 and 6-9)
    for i in range(0,4):
        home_row_keys[layout["row3"]["keys"][i]]=layout["row3"]["positions"][i]
    for i in range(6,10):
        home_row_keys[layout["row3"]["keys"][i]]=layout["row3"]["positions"][i]
    pass

    total_travel = 0
    #list containing (x_coordinate, home_row_key)
    x_coords = [(home_row_keys[key][0] , key) for key in home_row_keys]


    for char in input_string:
        #decide which finger
        if char.isupper():
            #assume left shift is pressed when rightside key, and vice versa
            home_row_key_used = findkey(x_coords, char.lower(), keymapping)
            right_shift_used = layout["row3"]["keys"].index(home_row_key_used) <= 3
            
            if right_shift_used:
                # adding key travel for shift
                point1 = keymapping["Shift_R"]
                point2 = layout["row3"]["positions"][-1]
                distance = np.sqrt(np.square(point2[1]-point1[1])+np.square(point2[0]-point1[0]))
                total_travel += distance
                # adding key travel for the main key
                point1 = keymapping[home_row_key_used] 
                point2 = keymapping[char.lower()]
                distance = np.sqrt(np.square(point2[1]-point1[1])+np.square(point2[0]-point1[0]))
                total_travel += distance
            else:
                point1 = keymapping["Shift_L"]
                point2 = layout["row3"]["positions"][0]
                distance = np.sqrt(np.square(point2[1]-point1[1])+np.square(point2[0]-point1[0]))
                total_travel += distance
                # adding key travel for the main key
                point1 = keymapping[home_row_key_used] 
                point2 = keymapping[char.lower()]
                distance = np.sqrt(np.square(point2[1]-point1[1])+np.square(point2[0]-point1[0]))
                total_travel += distance
        elif char.islower() or char.isnumeric():
            home_row_key_used = findkey(x_coords, char, keymapping) 
            point1 = keymapping[home_row_key_used] 
            point2 = keymapping[char]
            distance = np.sqrt(np.square(point2[1]-point1[1])+np.square(point2[0]-point1[0]))
            total_travel += distance
        else:
            try:
                home_row_key_used = findkey(x_coords, char, keymapping) 
                point1 = keymapping[home_row_key_used] 
                point2 = keymapping[char]
                distance = np.sqrt(np.square(point2[1]-point1[1])+np.square(point2[0]-point1[0]))
                total_travel += distance
            except:
                continue
        
    return total_travel

if __name__ == "__main__":
    # main function
    fig, ax = plt.subplots(figsize=(14, 8))  # generating axes object
    ax.set_xlim(-2, 16)  # Adjust limits based on key positions
    ax.set_ylim(-1, 6)
    ax.invert_yaxis()
    ax.set_aspect("equal")
    # plt.axohis('off')
    keymapping = genKeyboardLayout(ax, QWERTY_LAYOUT)
    x = np.array([1.5, 2.5, 3.5])
    y = np.array([0.5, 0.5, 0.5])
    frequencies = np.array([150, 8, 3])

    grid_size = (145, 40)  # Number of pixels in x and y``

    inputStr="Technology has significantly toransformed the way we live, work, and communicate. In the past few decades, advancements in fields such as computing, telecommunications, and artificial intelligence have revolutionized industries and reshaped society. From smartphones that connect us to the world instantly to automation that enhances efficiency in manufacturing, technology's impact is evident in every aspect of life. The rise of the internet has democratized access to information, enabling people to learn new skills, pursue opportunities, and interact with diverse cultures globally. Furthermore, AI and machine learning have introduced new possibilities in areas like healthcare, where predictive algorithms help diagnose diseases more accurately, and in transportation, where autonomous vehicles promise safer roads. However, with these advancements come challenges, including data privacy concerns, cybersecurity risks, and the potential displacement of jobs due to automation. As society continues to navigate this rapid technological evolution, it is essential to balance innovation with ethical considerations. Responsible development and regulation will play a crucial role in ensuring that technology continues to improve the quality of life for all, while mitigating its potential downsides. Ultimately, the future holds immense promise as technology continues to advance, but it requires careful stewardship to harness its full potential."
    #inputStr = "aaaaabb"
    print(len(inputStr))
    x, y, frequencies = genFreq(inputStr, keymapping)
    if len(sys.argv)>1:
        if sys.argv[1] == "-a":
            plot(inputStr, x, y, frequencies, gradual_decay, grid_size, ax, fig)
    else:
        plot1(inputStr, x, y, frequencies, gradual_decay, grid_size)
    distance = caculate_key_travel(keymapping, inputStr, QWERTY_LAYOUT)
    print(f"Total distance travelled is {distance} units")



    

