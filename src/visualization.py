import matplotlib.pyplot as plt

from algorithms import time_compareness
from grid import Grid


def grid_factory(width, height, cell_size, density):
    return Grid(None, height, width, cell_size, density)


def show_time_comparing():
    time_policy, time_value = time_compareness(grid_factory)

    labels1 = [str(key) for key in time_policy.keys()]
    times1 = list(time_policy.values())

    labels2 = [str(key) for key in time_value.keys()]
    times2 = list(time_value.values())

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6))

    ax1.bar(labels1, times1, color="maroon", width=0.4)
    ax1.set_xlabel("Grid Size, Wall Density")
    ax1.set_ylabel("Average Time")
    ax1.set_title("Policy Iteration")

    ax2.bar(labels2, times2, color="navy", width=0.4)
    ax2.set_xlabel("Grid Size, Wall Density")
    ax2.set_ylabel("Average Time")
    ax2.set_title("Value Iteration")

    plt.tight_layout()
    plt.show()

show_time_comparing()