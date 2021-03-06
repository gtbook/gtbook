# AUTOGENERATED! DO NOT EDIT! File to edit: display.ipynb (unless otherwise specified).

__all__ = ['show', 'pretty', 'randomImages', 'ROBOTS']

# Cell
import math
import gtsam
import graphviz
from .discrete import Variables
from .dbn import dbn_writer, has_positions


# Cell
class show(graphviz.Source):
    """ Display an object with a dot method as a graph."""

    def __init__(self, obj, *args, **kwargs):
        """Construct from object with 'dot' method."""
        # This small class takes an object, calls its dot function, and uses the
        # resulting string to initialize a graphviz.Source instance. This in turn
        # has a _repr_mimebundle_ method, which then renders it in the notebook.
        engine = "dot"

        # Check for Variables argument
        if args and isinstance(args[0], Variables):
            assert len(args) == 1, "Variables must be only positional argument."
            args = [args[0].keyFormatter()]

        # Check if a DotWriter needs creating (or amending)
        writer = dbn_writer(**kwargs)
        if writer is not None:
            kwargs = {"writer": writer}
            if has_positions(writer):
                engine = "neato"
        else:
            kwargs = {}

        # also switch to neato if NonlinearFactprGraph, as needs values always
        if isinstance(obj, gtsam.NonlinearFactorGraph):
            engine = "neato"
        super().__init__(obj.dot(*args, **kwargs), engine=engine)


# Cell
class pretty:
    """Render an object as html with optional arguments."""

    def __init__(self, obj, *args):
        if args and isinstance(args[0], Variables):
            assert len(args) == 1, "Variables must be only argument."
            variables = args[0]
            if isinstance(obj, gtsam.DiscreteValues):
                self._html = variables.values_html(obj)
            else:
                self._html = obj._repr_html_(
                    variables.keyFormatter(), variables.names())
        else:
            if isinstance(obj, gtsam.DiscreteValues):
                self._html = f"{obj}"
            elif isinstance(obj, gtsam.Pose2):
                x = round(obj.x(), 2)
                y = round(obj.y(), 2)
                theta = round(math.degrees(obj.theta()), 2)
                self._html = f"(x={x}, y={y}, theta={theta})"
            else:
                self._html = obj._repr_html_(*args)

    def _repr_html_(self):
        return self._html


# Cell
from IPython.display import HTML
import random

ROBOTS = ["Robot%20menagerie", "Trash%20sorting%20robot%20with%20gripper", "iRobot%20vacuuming%20robot", "Warehouse%20robots",
          "Two-wheeled%20Toy%20Robot", "Autonomous%20Vehicle%20with%20LIDAR%20and%20cameras", "Autonomous%20camera%20drone"]


def randomImages(ch: int, sec: int, style: str, nrImages: int, maxIndex: int = 8):
    """Create an HTML element with some random images.

    Args:
        ch (int): chapter number (base 1)
        sec (int): section number
        style (str): "cubist" | "steampunk" | "expressive"
        nrImages (int): number of images
        maxIndex (int, optional): Indexes to sample from. Defaults to 8.

    Returns:
        HTML: div with nrImages
    """
    perc = round(100/nrImages)
    robot = ROBOTS[ch-1]

    def image_tag(index):
        url = f"https://github.com/gtbook/robotics/blob/main/Art/{style}/S{ch}{sec}-{robot}-{index:02d}.jpg?raw=1"
        return f"<img src='{url}' style='height:256 width:{perc}%'/>"
    indices = random.sample(range(maxIndex), nrImages)
    return HTML(f"""
        <div align='center'>
        {" ".join([image_tag(index) for index in indices])}
        </div>
        """)
