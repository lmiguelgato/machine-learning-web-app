"""Initialize API module."""
import os

from .constant import LOCAL_STORAGE, MODEL_STORAGE, RPS_OPTIONS

# Create folders to store images if not existing
try:
    os.makedirs(MODEL_STORAGE, exist_ok=True)
    for v in RPS_OPTIONS.values():
        os.makedirs(LOCAL_STORAGE + "/" + v, exist_ok=True)
except FileExistsError:
    pass
