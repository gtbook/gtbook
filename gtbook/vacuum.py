# AUTOGENERATED! DO NOT EDIT! File to edit: vacuum.ipynb (unless otherwise specified).

__all__ = ['rooms', 'action_space', 'action_spec', 'light_levels', 'sensor_spec']

# Cell


# Cell
rooms = ["Living Room", "Kitchen", "Office", "Hallway", "Dining Room"]

# Cell
action_space = ["L", "R", "U", "D"]
action_spec = """
    1/0/0/0/0 2/8/0/0/0 1/0/0/0/0 2/0/0/8/0
    8/2/0/0/0 0/1/0/0/0 0/1/0/0/0 0/2/0/0/8
    0/0/1/0/0 0/0/2/8/0 0/0/1/0/0 0/0/1/0/0
    0/0/8/2/0 0/0/0/2/8 8/0/0/2/0 0/0/0/1/0
    0/0/0/8/2 0/0/0/0/1 0/8/0/0/2 0/0/0/0/1
    """

# Cell
light_levels = ["dark", "medium", "light"]
sensor_spec = "1/1/8 1/1/8 2/7/1 8/1/1 1/8/1"