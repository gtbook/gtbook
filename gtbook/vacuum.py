# AUTOGENERATED! DO NOT EDIT! File to edit: ../vacuum.ipynb.

# %% auto 0
__all__ = ['rooms', 'action_space', 'action_spec', 'light_levels', 'sensor_spec', 'calculate_value_system',
           'calculate_value_function']

# %% ../vacuum.ipynb 3
import numpy as np
import gtsam
from .discrete import Variables
from .display import pretty

# %% ../vacuum.ipynb 5
rooms = ["Living Room", "Kitchen", "Office", "Hallway", "Dining Room"]

# %% ../vacuum.ipynb 8
action_space = ["L", "R", "U", "D"]
action_spec = """
    1/0/0/0/0 2/8/0/0/0 1/0/0/0/0 2/0/0/8/0
    8/2/0/0/0 0/1/0/0/0 0/1/0/0/0 0/2/0/0/8
    0/0/1/0/0 0/0/2/8/0 0/0/1/0/0 0/0/1/0/0
    0/0/8/2/0 0/0/0/2/8 8/0/0/2/0 0/0/0/1/0
    0/0/0/8/2 0/0/0/0/1 0/8/0/0/2 0/0/0/0/1
    """

# %% ../vacuum.ipynb 12
light_levels = ["dark", "medium", "light"]
sensor_spec = "1/1/8 1/1/8 2/7/1 8/1/1 1/8/1"

# %% ../vacuum.ipynb 15
def calculate_value_system(
    R: np.array,  # reward function as a tensor
    T: np.array,  # transition probabilities as a tensor
    pi: np.array,  # policy, as a vector
    gamma=0.9,  # discount factor
):
    """Calculate A, b matrix of linear system for value computation."""
    b = np.empty((5,), float)
    AA = np.empty((5, 5), float)
    for x, room in enumerate(rooms):
        a = pi[x]  # action under policy
        b[x] = T[x, a] @ R[x, a]  # expected reward under policy pi
        AA[x] = -gamma * T[x, a]
        AA[x, x] += 1
    return AA, b


def calculate_value_function(
    R: np.array,  # reward function as a tensor
    T: np.array,  # transition probabilities as a tensor
    pi: np.array,  # policy, as a vector
    gamma=0.9,  # discount factor
):
    """Calculate value function for given policy"""
    AA, b = calculate_value_system(R, T, pi, gamma)
    return np.linalg.solve(AA, b)
