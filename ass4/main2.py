import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import animation

dimension = (5, 5)
fig, ax = plt.subplots(figsize=(3, 3))  # Reduce the figure size

# Create the heatmap with initial data
data = np.random.rand(*dimension)
heatmap = sns.heatmap(data, ax=ax, vmax=.8, cbar=False, annot=True, fmt=".2f")

def init():
    data = np.zeros(dimension)
    ax.clear()
    sns.heatmap(data, ax=ax, vmax=.8, cbar=False, annot=True, fmt=".2f")

# Define the animate function
def animate(i):
    data = np.random.rand(*dimension)
    ax.clear()
    sns.heatmap(data, ax=ax, vmax=.8, cbar=False, annot=True, fmt=".2f")
    return ax

# Create the animation
ani = animation.FuncAnimation(fig, animate, init_func=init, frames=20, repeat=False)
plt.show()

# Save the animation as a GIF with optimized parameters
ani.save('animated_heatmap.gif', writer='pillow', fps=2, dpi=80)