# marvelmind_donkeycar

Donkey plugin for the marvelmind indoor "GPS" system.

This branch makes a controllable avg_size and checks if the modul was initialised before data calling.


# How to build

in the project directory issue `python setuptools.py sdist`

# Install

After build one can install the package with pip: `pip install ./dist/<package>.tar.gz`

To patch donkeycar issue `patch_mm.sh patch`

# Uninstall

First undo donkeycar patches: `patch_mm.sh unpatch` or `unpatch_mm.sh`,
then `pip uninstall marvelmind-driver`.

# TODOS

* Check if safe work without isInit is possible.
* **Make patch mechanism more secure and fail-safe**
* Make post install scripts to automatically patch donkeycar

# Up for discussion:
* Should we create a different stop and destroy function? Are we ever gonna stop the data-reading without closing the connection?

# Done:

* Exception handling.
* Install and Uninstall.
* C-Python api usage in marvelmind api.