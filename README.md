# Testing nbdev

Playing with [nbdev](https://nbdev.fast.ai/).

## Notes while installing

- *Needs* `pip3 install -U nbdev`, not conda (has old version)
- lib_name seems to have to be the repo name in settings.ini
- After making changes to `settings.ini`, I run `nbdev_build_lib && nbdev_clean_nbs && nbdev_build_docs` to make sure all changes are propagated appropriately.
