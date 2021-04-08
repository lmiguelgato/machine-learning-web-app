"""Initialize API module
"""
import os
from os import listdir
from os.path import isfile, join

from .constant import (
    LOCAL_STORAGE,
    STORAGE_TRACKER,
    RPS_OPTIONS
    )


# Create folders to store images if not existing
try:
    for v in RPS_OPTIONS.values():
        os.makedirs(LOCAL_STORAGE + '/' + v, exist_ok=True)
except FileExistsError:
    pass

# Find all images in local storage, and group them by label
for index, label in RPS_OPTIONS.items():
    onlyfiles = [
        f for f in listdir(f"{LOCAL_STORAGE}/{label}/")
        if isfile(join(f"{LOCAL_STORAGE}/{label}/", f))     # TODO: ignore non-image files
        ]
    STORAGE_TRACKER[index] = onlyfiles
