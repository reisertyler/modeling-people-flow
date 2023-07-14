"""
Nonnegative Matrix Factorization

Date Created: Feb 8, 2023


"""

from src.python.utils import *

def sklearn_nmf(data_matrix, inner_k, init_mode='random'):
    """
    Perform Nonnegative Matrix Factorization using sklearn's NMF.
    """
    model = NMF(n_components=inner_k, init=init_mode, solver='cd', random_state=0)
    W = model.fit_transform(data_matrix)
    H = model.components_
    return W, H


def quick_nmf(data_matrix, inner_k):
    """
    Perform NMF and compute the relative error.
    """
    W, H = sklearn_nmf(data_matrix, inner_k, init_mode='nndsvdar')
    WH = np.dot(W, H)
    relative_error = np.linalg.norm(data_matrix - WH, 'fro') / np.linalg.norm(data_matrix, 'fro')
    return W, H, WH, relative_error


def plot_nmf_results(W, H, dates, k):
    """
    Plot the results of NMF.
    """
    plt.figure(figsize=(8,4))
    plt.title("NMF Results: Columns of W", size=12)
    plt.ylabel("Device Count", size=10)
    plt.xlabel("Time of Day", size=10)
    for i in range(k):
        plt.plot(dates, W[:,i], linewidth=1, label=str(i+1))
    plt.legend()
    plt.show()

    plt.figure(figsize=(8,3))
    plt.title("NMF Results: H (weighted)", size=14)
    plt.ylabel("Relative Contribution", size=10)
    plt.xlabel('Date')
    for i in range(k):
        plt.plot(H[i,:] * np.linalg.norm(W[:,i], 1) / 6, linewidth=1, label=str(i+1))
    plt.legend()
    plt.show()


def hockey_stick(data_matrix):
    """
    Plot the relative error vs. the inner dimension.
    """
    relative_errors = [quick_nmf(data_matrix, i)[3] for i in range(1, 20)]
    
    plt.figure(figsize=(10,4))
    plt.title("Study: Relative Error vs. Inner dimension ($k$)", size=12)
    plt.ylabel("Relative Contribution", size=12)
    plt.xlabel('Inner dimension, $k$', size=12)
    plt.plot(np.arange(1, 20), relative_errors, color='red', label=str(0+1))
    plt.show()


def nmf_study(data_matrix, dates, k):
    """
    Perform NMF and plot the results.
    """
    W, H, WH, relative_error = quick_nmf(data_matrix, k)
    plot_nmf_results(W, H, dates, k)
    return H, W, WH
