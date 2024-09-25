import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from collections import defaultdict
import matplotlib.colors as mcolors


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
        if row == "special_keys":
            continue
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
    x, y, z = list(),list(),list()

    for char in inpStr:
        try:
            coords = keyMapping[char]
           
            x.append(coords[0] + 0.5)
            y.append(coords[1] + 0.5)
            z.append(1)
        except:
            pass
    return x, y, z
    


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

    heatmap = np.zeros(grid_size)
    x_min, x_max = 0, 14.5
    y_min, y_max = 0, 4

    x_grid = np.linspace(x_min, x_max, grid_size[0])
    y_grid = np.linspace(y_min, y_max, grid_size[1])
    X, Y = np.meshgrid(x_grid, y_grid, indexing="xy")
    radius = 0.6

    def gradual_decay(distance, radius):
        return (1 - (distance / radius) ** 3) * (distance <= radius)

    # Example usage

    inputStr = "n today’s fast-paced world, the importance of connection cannot be overstated. With technology bridging gaps between distances, people find it easier than ever to communicate. Social media platforms, messaging apps, and video calls have transformed how we interact, making it possible to maintain relationships regardless of geographical barriers. However, this ease of communication often leads to superficial connections, where the depth of relationships may diminish. It’s crucial to strike a balance between digital interaction and meaningful in-person encounters. Engaging in face-to-face conversations fosters genuine connections that technology cannot replicate. Simple gestures like a warm smile, a hug, or sharing a laugh create memories that last a lifetime. Additionally, nurturing friendships requires effort; taking time to check in, share experiences, and be present for one another is essential. As we navigate through our busy lives, prioritizing real connections can lead to a more fulfilling existence. Whether it’s spending quality time with family or reconnecting with old friends, these moments enrich our lives and provide support in challenging times. Ultimately, the bonds we cultivate shape our experiences and contribute to our overall well-being, reminding us that, at the heart of life, connection is what truly matters."
    inputStr = "for a frustrated gamer"
    x, y, frequencies = genFreq(inputStr, keymapping)
    
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
        interpolation="bilinear",
        extent=[x_min, x_max, y_min, y_max],
        origin="lower",
        alpha=0.5,
    )
    plt.colorbar()

    # inputStr = "india"
    # coordinates_array = np.empty((-1,2))
    # for char in inputStr:
    #     coords = keymapping[char]
    #     coordinates_array = np.append(coordinates_array, [[coords[-1], coords[1]]], axis=0)

    # x = coordinates_array[:, -1]
    # y = coordinates_array[:, 0]

    plt.show()


# data = np.random.rand(10, 12)

# # Create a figure and axis
# fig, ax = plt.subplots(figsize=(10, 8))

# #draw the rectangle


# # Create a heatmap
# heatmap = ax.imshow(data, cmap='viridis', interpolation='bilinear')

# # Add rectangles in the background

# # Add a colorbar and title
# plt.colorbar(heatmap)
# plt.title('Heatmap with Rectangles in Background')
# plt.show()
