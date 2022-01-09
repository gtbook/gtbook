# AUTOGENERATED! DO NOT EDIT! File to edit: cli.ipynb (unless otherwise specified).

__all__ = ['rename', 'add_copyright']

# Cell
from pathlib import Path
from fastcore.script import call_parse

# Cell
@call_parse
def rename(dir: str  # dir in which to rename files
           ):
    """Rename notebooks to base 1 for chapters."""
    path = Path(dir)
    assert path.exists(), f"dir '{dir}' not found"
    assert path.is_dir(), f"'{dir}' is not a directory"
    print("Renaming notebooks now.")
    for ch in list(range(8, -1, -1)):
        print(f"Renaming chapter {ch}:")
        for x in path.glob(f"S{ch}*.ipynb"):
            new_name = path / x.name.replace(f"S{ch}", f"S{ch+1}")
            print(f"Renaming {x} to {new_name}")
            x.rename(new_name)


# Cell
@call_parse
def add_copyright():
    """Add copyright string to all specified files."""
    print("Addding copyright string.")
