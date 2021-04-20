"""Operations over images.
"""
import io
from datetime import datetime

import PIL.Image as Image

from api.constant import (
    RPS_OPTIONS,
    LOCAL_STORAGE
)


def check_image_format(uri, screenshot_format, selected):
    """Extract data from URI and check format and type of data received

    Args:
        data_uri (str): image in data URI format
        screenshot_format (str): data type and format
        selected: index of the options selected on the UI

    Returns:
        (bool, list of str): is data valid?, cause(s)
    """

    # Check format and type of data received
    tx_data_type, tx_data_format = screenshot_format.split('/')
    rx_data_type, rx_data_format = uri.mimetype.split('/')

    causes = []
    is_valid = True

    if tx_data_type != rx_data_type:
        is_valid = False
        causes.append(f"File type mismatch. Expected {tx_data_type}, got {rx_data_type}.")

    if tx_data_format != rx_data_format:
        is_valid = False
        causes.append(f"File format mismatch. Expected {tx_data_format}, got {rx_data_format}.")

    if rx_data_type != 'image':
        is_valid = False
        causes.append(f"Unexpected '{uri.mimetype}' received.")

    if selected not in RPS_OPTIONS:
        is_valid = False
        causes.append(f"Unexpected '{selected}' option.")

    return (is_valid, causes)


def save_capture(uri, selected, path=None):
    """Saves an image in data URI format, into the folder corresponding to the selected option

    Args:
        uri (data URI): image in data URI format
        selected (str): option selected

    Returns:
        bool, str: able to save image?, path to image
    """

    if path:
        save_path = f"{path}/"
    else:
        save_path = f"{LOCAL_STORAGE}/{RPS_OPTIONS[selected]}/"
    save_path += f"{RPS_OPTIONS[selected]}_{datetime.now().strftime('%Y-%m-%d_%H:%M:%S:%f')}"
    save_path += f".{uri.mimetype.split('/')[1]}"

    image = Image.open(io.BytesIO(uri.data))
    image.save(save_path)

    return True, save_path
