"""Initialize API module
"""
import os

from .constant import (
    LOCAL_STORAGE,
    RPS_OPTIONS
    )


# Create folders to store images if not existing
try:
    for v in RPS_OPTIONS.values():
        os.makedirs(LOCAL_STORAGE + '/' + v, exist_ok=True)
except FileExistsError:
    pass
