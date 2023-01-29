# AUTOGENERATED! DO NOT EDIT! File to edit: ../drone.ipynb.

# %% auto 0
__all__ = ['axes_figure', 'axes']

# %% ../drone.ipynb 3
import math
import numpy as np
import plotly.express as px
import pandas as pd
import gtsam

# %% ../drone.ipynb 5
def axes_figure(pose: gtsam.Pose3, scale: float = 1.0, labels: list = ["X", "Y", "Z"]):
    """Create plotly express figure with Pose3 coordinate frame."""
    t = np.reshape(pose.translation(),(3,1))
    M = np.hstack([t,t,t,pose.rotation().matrix() * scale + t])
    df = pd.DataFrame({"x": M[0], "y": M[1], "z": M[2]}, labels+labels)
    return px.line_3d(df, x="x", y="y", z="z", color=df.index,
                     color_discrete_sequence=["red", "green", "blue"])

def axes(*args, **kwargs):
    """Create 3 Scatter3d traces representing Pose3 coordinate frame."""
    return axes_figure(*args, **kwargs).data
