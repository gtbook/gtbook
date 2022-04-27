# AUTOGENERATED! DO NOT EDIT! File to edit: gaussian.ipynb (unless otherwise specified).

__all__ = ['sample_conditional', 'sample_bayes_net']

# Internal Cell
import gtsam
import numpy as np
import plotly.express as px
import pandas as pd

# Cell
def sample_conditional(node: gtsam.GaussianConditional, N: int, parents: list = [], sample: dict = {}):
    """Sample from conditional """
    # every node ~ exp(0.5*|R x + S p - d|^2)
    # calculate mean as inv(R)*(d - S p)
    d = node.d()
    n = len(d)
    rhs = d.reshape(n, 1)
    if len(parents) > 0:
        rhs = rhs - node.S() @ np.vstack([sample[p] for p in parents])
    # sample from conditional Gaussian
    invR = np.linalg.inv(node.R())
    return invR @ (rhs + np.random.normal(size=(n, N)))


def sample_bayes_net(bn: gtsam.GaussianBayesNet, N: int) -> dict:
    """ High performance ancestral sampling.
        It returns a dictionary of nj x N samples, where n_j is the dimensionality for key j.
    """
    sample = {}
    for i in reversed(range(bn.size())):
        conditional = bn.at(i)
        key, *parents = conditional.keys()
        sample[key] = sample_conditional(bn.at(i), N, parents, sample)
    return sample