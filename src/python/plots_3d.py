"""
Plotting the data

Date Created: Feb 8, 2023


"""

from src.python.utils import *

def plot_3d_single(data, k):
    """
    Plot the data in 3D. This is just a good visual for what the first plot is showing.
    """
    num_points = len(data)
    x = np.arange(0, num_points)

    fig = plt.figure(figsize=(8,8))
    ax = fig.add_subplot(projection="3d")
    ax.view_init(elev=15., azim=-125)
    ax.set_xlabel('Time of Day', size=14)
    ax.set_ylabel('Day', size=14)
    ax.set_zlabel('Device Count', size=14)

    for i in range(k):
        ax.plot(x, data.T[i], i, zdir='y', color='blue', linewidth=0.7)
    plt.show()