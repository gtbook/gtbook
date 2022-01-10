# AUTOGENERATED! DO NOT EDIT! File to edit: display.ipynb (unless otherwise specified).

__all__ = ['show', 'pretty', 'randomImages', 'ROBOTS']

# Cell
import gtsam
import graphviz
from .discrete import Variables

# Cell
class show(graphviz.Source):
    """ Display an object with a dot method as a graph."""

    def __init__(self, obj, *args, **kwargs):
        """Construct from object with 'dot' method."""
        # This small class takes an object, calls its dot function, and uses the
        # resulting string to initialize a graphviz.Source instance. This in turn
        # has a _repr_mimebundle_ method, which then renders it in the notebook.
        if args and isinstance(args[0], Variables):
            assert len(args) == 1, "Variables must be only argument."
            keyFormatter = args[0].keyFormatter()
            super().__init__(obj.dot(keyFormatter))
        else:
            super().__init__(obj.dot(*args, **kwargs))

# Cell
class pretty:
    """Render an object as html with optional arguments."""

    def __init__(self, obj, *args):
        if args and isinstance(args[0], Variables):
            assert len(args) == 1, "Variables must be only argument."
            variables = args[0]
            if isinstance(obj, gtsam.DiscreteValues):
                self._md = variables.values_html(obj)
            else:
                self._md = obj._repr_html_(
                    variables.keyFormatter(), variables.names())
        else:
            if isinstance(obj, gtsam.DiscreteValues):
                self._md = f"{obj}"
            else:
                self._md = obj._repr_html_(*args)

    def _repr_html_(self):
        return self._md


# Cell
from IPython.core.display import HTML
import random

ROBOTS = ["Robot menagerie", "Trash sorting robot with Gripper", "iRobot vacuuming robot", "Warehouse robots",
          "Two-wheeled Toy Robot", "Autonomous Vehicle with LIDAR and cameras", "Autonomous camera drone"]


def randomImages(ch: int, sec: int, style: str, nrImages: int, maxIndex: int = 8):
    """Create an HTML element with some random images.

    Args:
        ch (int): chapter number
        sec (int): section number
        style (str): "cubist" | "steampunk" | "expressive"
        nrImages (int): number of images
        maxIndex (int, optional): Indexes to sample from. Defaults to 8.

    Returns:
        HTML: div with nrImages
    """
    perc = round(100/nrImages)
    robot = ROBOTS[ch]

    def image_tag(index):
        url = f"https://github.com/gtbook/robotics/blob/main/Art/{style}/S{ch}{sec}-{robot}-{index:02d}.jpg?raw=1"
        return f"<img src='{url}' style='height:256 width:{perc}%'/>"
    indices = random.sample(range(maxIndex), nrImages)
    return HTML(f"""
        <div align='center'>
        {" ".join([image_tag(index) for index in indices])}
        </div>
        """)
