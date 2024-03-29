# AUTOGENERATED! DO NOT EDIT! File to edit: ../nerf.ipynb.

# %% auto 0
__all__ = []

# %% ../nerf.ipynb 3
from dataclasses import dataclass
import json
import numpy as np
import torch.nn.functional as F

import PIL
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset

# %% ../nerf.ipynb 4
WHITE = torch.full((3,), 1.0, dtype=torch.float)
BLACK = torch.full((3,), 0.0, dtype=torch.float)
DEVICE = (
    torch.device("cuda") if torch.cuda.is_available()
    else torch.device("mps") if torch.backends.mps.is_available()
    else torch.device("cpu")
)
print(f"Using device: {DEVICE}")
