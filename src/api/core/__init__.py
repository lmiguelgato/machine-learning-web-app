"""Initialize module requirements
"""
import os


# Create folders to store images if not existing
try:
    os.makedirs('./data/rock', exist_ok=True)
    os.makedirs('./data/paper', exist_ok=True)
    os.makedirs('./data/scissor', exist_ok=True)
except FileExistsError:
    pass
