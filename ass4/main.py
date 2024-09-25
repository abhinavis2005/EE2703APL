import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

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
            (13, 0),  # Added space for Backspace key
        ],
    },
    "row2": {
        "keys": "qwertyuiop[]\\",
        "positions": [
            (0.5, 1),
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
        ],
    },
    "row3": {
        "keys": "asdfghjkl;'",
        "positions": [
            (0.75, 2),
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
        ],
    },
    "row4": {
        "keys": "zxcvbnm,./",
        "positions": [
            (1.25, 3),
            (2.25, 3),
            (3.25, 3),
            (4.25, 3),
            (5.25, 3),
            (6.25, 3),
            (7.25, 3),
            (8.25, 3),
            (9.25, 3),
            (10.25, 3),
        ],
    },
    "special_keys": {
        "Shift_L": (0, 3),
        "Shift_R": (11.25, 3),
        "Space": (3.5, 4),
        "Backspace": (13, 0),
        "Tab": (0, 1),
        "CapsLock": (0, 2),
        "Enter": (12, 2),
    },
}

def genKeyboardLayout(ax: plt.axes, layout: dict):
    for row in layout:
        if row == "special_keys":
            continue
        for index, key in enumerate(layout[row]["keys"]):
            pos = layout[row]["positions"][index]
            rect = Rectangle(pos, 1, 1, edgecolor='black', linewidth=1, facecolor='lightgray')
            ax.add_patch(rect)
            ax.text(pos[0] + 0.5, pos[1] + 0.5, key, ha='center', va='center', color='black')

    # Draw special keys
    for key, pos in layout["special_keys"].items():
        rect = Rectangle(pos, 1.5, 1, edgecolor='black', linewidth=1, facecolor='lightgray')
        ax.add_patch(rect)
        ax.text(pos[0] + 0.75, pos[1] + 0.5, key, ha='center', va='center', color='black')

if __name__ == '__main__':
    # Main function 
    fig, ax = plt.subplots(figsize=(10, 8))  # Generating axes object
    genKeyboardLayout(ax, QWERTY_LAYOUT)
    
    # Set axis limits and aspect
    ax.set_xlim(-1, 14)  # Adjust limits based on key positions
    ax.set_ylim(-1, 5)
    ax.set_aspect('equal')
    ax.axis('off')  # Hide the axis

    plt.show()
