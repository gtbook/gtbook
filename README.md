# gtbook
> An <a href='https://nbdev.fast.ai/'>nbdev</a> powered toolbox for Frank and Seth's robotics book.


## How to use

In the book chapters, we should have a cell that fetches the latest version using pip:

```bash
%pip install -q -U gtbook
```

The above automatically installs other libraries on colab, e.g., gtsam and plotly.

You also need a cell that imports what you need in a particular section, for example:

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
- `nbdev_prepare` to prepare for git commit

To release a new version:

- nbdev_bump_version
- make release

Problems with nbdev2:

- Somehow still wants to build the website in "docs"
- "fixes" the notebooks in test, making cli test fail (commented out now). I committed them as I don't know how to prevent this. Correct files are at tag "nbdev1"

Problems with circular dependency and issue [#3](https://github.com/gtbook/gtbook/issues/3), January 2023:

- By adding the pybind stl header again in inference.h the typeError went away
- building the wrapper in 3.8 leads to a circular dependency, however.
- I created a version 4.2a9 to stabilize, and created a PR on gtsam-manylinux-build to build it. It builds and wheels were built for linux and mac-86.
- I built 3 wheels for M1 with gtsam-build-m1.
- uploaded all with twine, at https://pypi.org/project/gtsam/4.2a9/
- changed dependence to 4.2a9
- nbdev_prepare and nbdev_pypi