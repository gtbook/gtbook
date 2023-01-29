# gtbook
> An <a href='https://nbdev.fast.ai/'>nbdev</a> powered toolbox for Frank and Seth's robotics book.


## How to use

In the book chapters, we should have a cell that fetches the latest version using pip:

```bash
%pip install -q -U gtbook
```

The above automatically installs other libraries on colab, e.g., gtsam and plotly.

You also needs a cell that imports what you need in a particular section, for example:

```python
from gtbook.display import show
from gtbook.discrete import Variables
```
Further usage examples of these and more functions are given in the module documentation itself.

There are also some command line tools defined in the `cli` module.

## Notes for development

> Mostly for Frank as he adds to the library.

- Conda install nbdev
- show preview using `nbdev_preview`
- `pip install -e .` for local install for test purposes.
- `nbdev_prepare` to prepare for git commit, but don't commit changes in test folder.

To release a new version:

- nbdev_bump_version
- make release
