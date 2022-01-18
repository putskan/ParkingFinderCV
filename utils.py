import pickle
import os
from constants import RECTANGLES_FILEPATH


def load_pos_list():
    if os.path.exists(RECTANGLES_FILEPATH):
        with open(RECTANGLES_FILEPATH, "rb") as f:
            return pickle.load(f)
    return []
