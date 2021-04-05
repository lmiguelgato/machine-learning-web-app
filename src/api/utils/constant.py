"""Constants definition and initialization
"""
import os


LOCAL_STORAGE = './data'

RPS_OPTIONS = {
    '0': 'rock',
    '1': 'paper',
    '2': 'scissor'
}

# Create folders to store images if not existing
try:
    for v in RPS_OPTIONS.values():
        os.makedirs(LOCAL_STORAGE + '/' + v, exist_ok=True)
except FileExistsError:
    pass
