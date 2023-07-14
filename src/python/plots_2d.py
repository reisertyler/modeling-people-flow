"""
Plotting the data

Date Created: Feb 8, 2023


"""

from src.python.utils import *

def view_data_embed(data_matrix, dates):
    """
    Plot all days in the study on one plot.
    """
    num_rows, num_columns = data_matrix.shape
    plt.figure(figsize=(8,4))
    for i in range(num_columns):
        plt.plot(dates, data_matrix[:,i], color='blue', linewidth=.5) 
    plt.title("Study: Data Embedding", size=14)
    plt.ylabel("Usercount", size=14)
    plt.xlabel("Time of Day")
    plt.margins(x=0)
    plt.show()


def view_data(data_matrix, dates, build_date, show):
    """
    Break the plot into pieces so weekly intervals, or any other interval the userdefines,
    using the 'show' value.
    """
    num_rows, num_columns = data_matrix.shape
    blocks = math.ceil(num_columns / show)
    plt.figure(figsize=(8,18))
    plt.title("Study: Data Embedding", size=14)
    for block in range(blocks):
        plt.subplot(blocks, 1, block + 1)
        plt.ylabel("Usercount", size=14)
        start = block * show
        stop = min(start + show, num_columns)
        for i in range(start, stop):
            plt.plot(dates, data_matrix[:,i], linewidth=0.8, label=str(build_date[i])[1:])
        plt.legend()
    plt.xlabel('Time of Day')
    plt.show()
