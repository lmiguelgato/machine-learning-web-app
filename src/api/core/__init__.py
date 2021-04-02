import os


try:
    os.makedirs('./data/rock', exist_ok=True)
    os.makedirs('./data/paper', exist_ok=True)
    os.makedirs('./data/scissor', exist_ok=True)
except FileExistsError:
    pass
