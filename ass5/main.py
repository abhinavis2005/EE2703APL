import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import matplotlib.colors as mcolors
import qwerty_layout
import random
from matplotlib.animation import FuncAnimation

def gradual_decay(distance, radius):
    """
    an algebraic function that decays as (1-x/r^3) inside 
    a circle of radius r, helps in creating the decay effect for the heatmap
    """
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
        keys = characters[char] #keys to be pressed
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
    ax
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

    ax.imshow(
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
            start_pos = layout[key]["start"]  # home row key to be used
            pos1 = start_pos
            pos2 = layout[key]["pos"]
            distance = np.sqrt((pos2[1] - pos1[1]) ** 2 + (pos2[0] - pos1[0]) ** 2)
            sum += distance
    return sum

def layout_update(keys:dict) -> dict:
    """
    Takes in the initial layout, and changes the 
    start from a str(name of the home row key) to the
    pos (coordinates) of the home row key
    """
    for key in keys:
        key_data = keys[key]
        key_data['start'] = keys[key_data['start']]['pos']
    return keys

def neighbour_solution(keys:dict) -> dict:
    """
    generates a neighbour layout to the given layout
    for simulated annealing, by sampling from the 
    keys of the dictionary, excluding the special 
    characters
    We dont want solutions where shift, tab etc go 
    to the middle of they keyboard """
    new_keys = keys.copy()
    # dont swap special keys
    
    i, j = random.sample(list(keys.keys())[:-7],2)
    #only keys themselves change, not pos or homerow key
    new_keys[i], new_keys[j] = new_keys[j], new_keys[i] 
    return new_keys

def simulated_annealing(layout:dict, initial_temp:float, cooling_rate:float, num_itreations:int, inpString:str)->tuple[list, list, dict]:
    
    temp = initial_temp #initial conditions
    current_distance = caculate_key_travel(inpString, layout.keys, layout.characters)
    current_layout= layout.keys.copy()
    
    #best conditions
    best_layout = current_layout
    best_distance = current_distance

    distances = [current_distance]
    best_distances = [best_distance]

    for _ in range(num_itreations):
        neighbour_layout = neighbour_solution(current_layout)
        neighbour_distance = caculate_key_travel(inpString, neighbour_layout, layout.characters)
        arg = (current_distance - neighbour_distance)/ temp
        max_val = 700

        p = np.exp(np.clip(arg, None, 700))# probability

        if neighbour_distance < current_distance or random.random() < p:
            current_distance = neighbour_distance
            current_layout = neighbour_layout

            if current_distance < best_distance:
                best_layout = current_layout.copy()
                best_distance = current_distance
        
        temp *= cooling_rate
        distances.append(current_distance)
        best_distances.append(best_distance)

    return best_distances, distances, best_layout

def update(frame, best_distances, distances, best_distance_line, distance_line):
    distance_line.set_data(range(frame+1), distances[:frame+1])
    best_distance_line.set_data(range(frame+1), best_distances[:frame+1])
    return distance_line, best_distance_line


if __name__ == "__main__":

    fig, ax1 = plt.subplots(1,1, figsize=(14, 8))  # generating axes , fig object
   
    layout = qwerty_layout


    inputStr = input("Enter string : ")
    layout_update(layout.keys) #changing the layout to be compatible for simulated annealing

    #hyperparameters
    initial_temp = 1000
    cooling_rate = 0.98
    num_iterations = 1000
    best_distances, distances, best_layout = simulated_annealing(layout, initial_temp, cooling_rate, num_iterations, inputStr)

    #  simulated annealing plot
    ax1.set_title("Simulated Annealing Distance vs Iterations")
    ax1.set_xlim(0, num_iterations)
    ax1.set_ylim(min(best_distances)*0.9, max(distances)*1.1)
    distance_line, = ax1.plot([],[], 'r-')
    best_distance_line, = ax1.plot([],[], 'g-')

   
    #generating animation
    anim = FuncAnimation(fig, update, frames = range(0, num_iterations,15), fargs=(best_distances, distances, best_distance_line, distance_line), 
                         interval =0, blit=True, repeat=False)
    anim.save('animation.gif', writer='pillow', fps=30)

    #heatmap generation
    grid_size = (58, 16)  # Number of pixels in x and y`
    fig1, ax = plt.subplots(1, 1, figsize=(14,8))
    ax.set_title("Optimized Keyboard Heatmap")
    ax.set_xlim(-2, 16)
    ax.set_ylim(-1, 6)
    ax.set_aspect("equal")
    ax.axis("off")
    genKeyboardLayout(ax, best_layout)
    x, y = genFreq(inputStr, best_layout, layout.characters)
    plot1(x, y, grid_size, ax)
    fig1.savefig('heatmap.png', bbox_inches='tight')

    
    print(f"Total distance travelled after optimization is {best_distances[-1]} units")
