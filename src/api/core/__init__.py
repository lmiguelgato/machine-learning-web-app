import os


try:
    os.mkdir('data')
except FileExistsError:
    pass
