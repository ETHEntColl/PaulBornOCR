import os
from os import write

import pyautogui
import pyperclip
import pytesseract

DEFAULT_CONFIDENCE = 0.9


def get_current_username():
    """
    Determine the username of the current user based on the os.getcwd command (directory after Users).
    If that doesn't work, try using os.getlogin().

    Returns
    -------
    str
        The username of the current user.
    """
    try:
        # Attempt to get the username from the current working directory
        cwd = os.getcwd()
        parts = cwd.split(os.sep)
        if 'Users' in parts:
            user_index = parts.index('Users') + 1
            if user_index < len(parts):
                return parts[user_index]
    except Exception as e:
        print(f"Failed to get username from os.getcwd(): {e}")

    try:
        # Fallback to using os.getlogin()
        return os.getlogin()
    except Exception as e:
        print(f"Failed to get username from os.getlogin(): {e}")
        return None

def set_tesseract_path():
    """
    Set the Tesseract path for pytesseract.
    """

    pytesseract.pytesseract.tesseract_cmd = fr'C:\Users\{get_current_username()}\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'   # pyautogui.moveTo(COORDINATES['collector_add'])

def input_field_from_label(image_name, confidence=DEFAULT_CONFIDENCE):
    """
    Determine the coordinates of an input field based on the label image.

    Parameters
    ----------
    image_name : str
        The filename of the label image.
    confidence : float
        The confidence threshold for image matching.

    Returns
    -------
    tuple
        The coordinates of the input field.
    """
    label_location = pyautogui.locateCenterOnScreen(os.path.join('imgs', image_name), confidence=confidence)
    input_field_location = (label_location[0] + 100, label_location[1])
    return input_field_location

def determine_coordinates(confidence: float = DEFAULT_CONFIDENCE, verbose: bool = False) -> dict:
    """
    Determine the coordinates of various elements on the screen.

    Parameters
    ----------
    confidence : float
        The confidence threshold for image matching.
    verbose : bool
        Whether to print the found coordinates.

    Returns
    -------
    dict
        A dictionary containing the coordinates of various elements.
    """
    print("Determining coordinates. Don't move the mouse or change the screen layout...")

    COORDINATES = {}

    try:
        COORDINATES['previous'] = pyautogui.locateCenterOnScreen('imgs/previous.png', confidence=confidence)
    except pyautogui.ImageNotFoundException:
        COORDINATES['previous'] = pyautogui.locateCenterOnScreen('imgs/previous_deactivated.png', confidence=confidence)
    try:
        COORDINATES['next'] = pyautogui.locateCenterOnScreen('imgs/next.png', confidence=confidence)
    except pyautogui.ImageNotFoundException:
        COORDINATES['next'] = pyautogui.locateCenterOnScreen('imgs/next_deactivated.png', confidence=confidence)

    COORDINATES['save'] = pyautogui.locateCenterOnScreen('imgs/save.png', confidence=confidence)
    COORDINATES['pinlabels'] = pyautogui.locateCenterOnScreen('imgs/pinlabels.png', confidence=confidence)
    COORDINATES['count'] = pyautogui.locateCenterOnScreen('imgs/images.png', confidence=confidence)
    COORDINATES['numbers_more_button'] = pyautogui.locateCenterOnScreen('imgs/numbers_more_button.png', confidence=confidence)
    COORDINATES['numbers_more_number'] = (COORDINATES['numbers_more_button'][0] + 100, COORDINATES['numbers_more_button'][1])
    COORDINATES['numbers_more_type'] = (COORDINATES['numbers_more_button'][0] + 600, COORDINATES['numbers_more_button'][1])
    COORDINATES['collector_add'] = pyautogui.locateCenterOnScreen('imgs/collector.png', confidence=confidence)
    COORDINATES['collector_name'] = (COORDINATES['collector_add'][0] + 65, COORDINATES['collector_add'][1])
    COORDINATES['workflow_status'] = input_field_from_label('workflow_status.png', confidence)
    COORDINATES['collection'] = input_field_from_label('collection.png', confidence)
    COORDINATES['date_verbatim'] = input_field_from_label('date_verbatim.png', confidence)
    COORDINATES['date_interpreted'] = input_field_from_label('date_interpreted.png', confidence)
    COORDINATES['taxon'] = input_field_from_label('associated_taxon.png', confidence)
    COORDINATES['elevation_from'] = input_field_from_label('elevation_from.png', confidence)
    COORDINATES['elevation_to'] = input_field_from_label('elevation_to.png', confidence)
    COORDINATES['specimen_notes'] = input_field_from_label('notes.png', confidence)
    COORDINATES['sex'] = input_field_from_label('sex.png', confidence)

    print("Finished determining coordinates.")

    if verbose:
        print("Coordinates:")
        for k, v in COORDINATES.items():
            print(f'{k}: {v}')
        print('-' * 40)

    return COORDINATES

# Determine the coordinates once at the beginning
COORDINATES = determine_coordinates(verbose=True)
set_tesseract_path()


def write_with_clipboard(text_to_write, coordinates=None):
    """
    Save the current clipboard content to a variable, copy the text to write into the clipboard,
    paste it, and then restore the original clipboard content.

    Args:
        text_to_write (str): The text to write using the clipboard.
    """

    if isinstance(coordinates, str):
        coordinates = COORDINATES[coordinates]

    if coordinates is not None:
        # Click the button first
        pyautogui.click(coordinates)

    # Save the current clipboard content
    temp = pyperclip.paste()

    # Copy the text to write into the clipboard
    pyperclip.copy(text_to_write)

    # Paste the text
    pyautogui.hotkey('ctrl', 'v')

    # Restore the original clipboard content
    pyperclip.copy(temp)

def perform_previous(position_after=None, pinlabels=True):
    if position_after is None:
        position_after = pyautogui.position()
    pyautogui.click(COORDINATES['previous'])
    if pinlabels:
        pyautogui.click(COORDINATES['pinlabels'])
    pyautogui.moveTo(position_after)

def perform_next(position_after=None, pinlabels=True):
    if position_after is None:
        position_after = pyautogui.position()
    pyautogui.click(COORDINATES['next'])
    if pinlabels:
        pyautogui.click(COORDINATES['pinlabels'])
    pyautogui.moveTo(position_after)

def perform_save():
    pyautogui.hotkey('alt', 's')

def perform_actions_collection(collection_name):
    write_with_clipboard(collection_name, 'collection')
    pyautogui.press('enter')

def perform_actions_collector(text_to_type):
    pyautogui.click(COORDINATES['collector_add'])
    write_with_clipboard(text_to_type, 'collector_name')
    pyautogui.press('enter')

def perform_actions_numbers_more(number, number_type):
    # Click the button first
    pyautogui.click(COORDINATES['numbers_more_button'])
    # Fill in the fields
    pyautogui.click(COORDINATES['numbers_more_number'])
    pyautogui.typewrite(str(number))
    write_with_clipboard(number_type, 'numbers_more_type')
    pyautogui.press('enter')

def perform_actions_date(text_to_type_verbatim, text_to_type_intrp):
    write_with_clipboard(text_to_type_verbatim, 'date_verbatim')
    write_with_clipboard(text_to_type_intrp, 'date_interpreted')

def perform_actions_taxon(taxon_name):
    write_with_clipboard(taxon_name, 'taxon')

def perform_actions_height(el_from, el_to):
    write_with_clipboard(el_from, 'elevation_from')
    write_with_clipboard(el_to, 'elevation_to')

def perform_actions_notes(text_to_type):
    write_with_clipboard(text_to_type, 'specimen_notes')

def perform_actions_sex(sex):
    write_with_clipboard(sex.capitalize(), 'sex')
    pyautogui.press('enter')

def perform_actions_workflow_status(status):
    # write_with_clipboard(status, input_field_from_label('workflow_status.png'))
    write_with_clipboard(status, 'workflow_status')
    pyautogui.press('enter')

