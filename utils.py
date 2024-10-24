import os
import time

import pyautogui
import pyperclip
import pytesseract
from pyautogui import click

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

def set_tesseract_path(username=None):
    """
    Set the Tesseract path for pytesseract.

    Parameters
    ----------
    username : str
        The username of the current user
    """
    if username is None:
        username = get_current_username()

    pytesseract.pytesseract.tesseract_cmd = fr'C:\Users\{username}\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'


class ScreenAutomation:
    def __init__(self, confidence: float = 0.9, add_determination: bool = False, verbose: bool = False):
        """
        Initializes the ScreenAutomation class by determining the coordinates of various elements on the screen.

        Parameters
        ----------
        confidence : float
            The confidence threshold for image matching.
        add_determination : bool
            Whether to add the determination coordinates.
        verbose : bool
            Whether to print the found coordinates.
        """
        # Store all parameters as instance attributes
        self.confidence = confidence
        self.add_determination = add_determination
        self.verbose = verbose

        # Determine coordinates and store them as an instance attribute
        self.coordinates = self._determine_coordinates()

    def _determine_coordinates(self) -> dict:
        """
        Determine the coordinates of various elements on the screen.

        Returns
        -------
        dict
            A dictionary containing the coordinates of various elements.
        """
        print("Determining coordinates. Don't move the mouse or change the screen layout...")

        coordinates = {}

        try:
            coordinates['previous'] = self.input_field_from_label('previous.png')
        except pyautogui.ImageNotFoundException:
            coordinates['previous'] = self.input_field_from_label('previous_deactivated.png')
        try:
            coordinates['next'] = self.input_field_from_label('next.png')
        except pyautogui.ImageNotFoundException:
            coordinates['next'] = self.input_field_from_label('next_deactivated.png')

        coordinates['save'] = self.input_field_from_label('save.png')
        coordinates['pinlabels'] = self.input_field_from_label('pinlabels.png')
        coordinates['count'] = self.input_field_from_label('images.png')
        coordinates['numbers_more_button'] = self.input_field_from_label('numbers_more_button.png')
        coordinates['numbers_more_number'] = (
        coordinates['numbers_more_button'][0] + 100, coordinates['numbers_more_button'][1])
        coordinates['numbers_more_type'] = (
        coordinates['numbers_more_button'][0] + 600, coordinates['numbers_more_button'][1])
        coordinates['collector_add'] = self.input_field_from_label('collector.png')
        coordinates['collector_name'] = (coordinates['collector_add'][0] + 65, coordinates['collector_add'][1])
        coordinates['workflow_status'] = self.input_field_from_label('workflow_status.png', 100, 0)
        coordinates['collection'] = self.input_field_from_label('collection.png', 100, 0)
        coordinates['date_verbatim'] = self.input_field_from_label('date_verbatim.png', 100, 0)
        coordinates['date_interpreted'] = self.input_field_from_label('date_interpreted.png', 100, 0)
        coordinates['taxon'] = self.input_field_from_label('associated_taxon.png', 100, 0)
        coordinates['elevation_from'] = self.input_field_from_label('elevation_from.png', 100, 0)
        coordinates['elevation_to'] = self.input_field_from_label('elevation_to.png', 100, 0)
        coordinates['specimen_notes'] = self.input_field_from_label('notes.png', 100, 0)
        coordinates['sex'] = self.input_field_from_label('sex.png', 100, 0)

        if self.add_determination:
            print("Adding determination coordinates")
            column_names_numbers = [
                ('det_genus', 1),
                ('det_species', 2),
                ('det_subspecies', 3),
                ('det_infraspecific', 4),
                ('det_infrarank', 5),
                ('det_author', 6),
                ('det_determiner', 8),
                ('det_date', 12),
                ('det_verbatim', 10)
            ]
            column_width = 90
            coordinates['det_button'] = self.input_field_from_label('det_button.png')
            pyautogui.click(coordinates['det_button'])
            time.sleep(0.5)
            coordinates['det_add_button'] = self.input_field_from_label('det_add_button.png')
            coordinates['det_done_button'] = self.input_field_from_label('det_done_button.png')
            coordinates_first_column = self.input_field_from_label('det_species_number.png')
            for column_name, column_number in column_names_numbers:
                coordinates[column_name] = (
                    coordinates_first_column[0] + column_width * column_number,
                    coordinates_first_column[1] + 25
                )
            pyautogui.click(coordinates['det_done_button'])

        print("Finished determining coordinates.")

        if self.verbose:
            print("Coordinates:")
            for k, v in coordinates.items():
                print(f'{k}: {v}')
            print('-' * 40)

        return coordinates

    def input_field_from_label(self, image_name, x_offset=0, y_offset=0, confidence=None):
        """
        Determine the coordinates of an input field based on the label image.

        Parameters
        ----------
        image_name : str
            The filename of the label image.
        x_offset : int
            The x offset from the label location.
        y_offset : int
            The y offset from the label location.
        confidence : float
            The confidence threshold for image matching.

        Returns
        -------
        tuple
            The coordinates of the input field.
        """
        if confidence is None:
            confidence = self.confidence

        # Locate the label image on screen
        label_location = pyautogui.locateCenterOnScreen(os.path.join('imgs', image_name), confidence=confidence)

        # Check if label_location is found, to prevent crashes if the image is not found
        if label_location is None:
            raise pyautogui.ImageNotFoundException(f"Label image {image_name} not found on screen.")

        # Calculate the input field location based on the offsets
        input_field_location = (label_location[0] + x_offset, label_location[1] + y_offset)
        return input_field_location

    def write_with_clipboard(self, text_to_write, coordinates=None, **pyautogui_click_kwargs):
        """
        Save the current clipboard content, copy the text to write into the clipboard,
        paste it, and then restore the original clipboard content.

        Parameters
        ----------
        text_to_write : str
            The text to write using the clipboard.
        coordinates : str or tuple
            The coordinates to click before writing the text.
        """

        if isinstance(coordinates, str):
            coordinates = self.coordinates[coordinates]

        if coordinates is not None:
            # Click the button first
            pyautogui.click(coordinates, **pyautogui_click_kwargs)

        # Save the current clipboard content
        temp = pyperclip.paste()

        # Copy the text to write into the clipboard
        pyperclip.copy(text_to_write)

        # Paste the text
        pyautogui.hotkey('ctrl', 'v')

        # Restore the original clipboard content
        pyperclip.copy(temp)

    def perform_previous(self, position_after=None, pinlabels=True):
        if position_after is None:
            position_after = pyautogui.position()
        pyautogui.click(self.coordinates['previous'])
        if pinlabels:
            pyautogui.click(self.coordinates['pinlabels'])
        pyautogui.moveTo(position_after)

    def perform_next(self, position_after=None, pinlabels=True):
        if position_after is None:
            position_after = pyautogui.position()
        pyautogui.click(self.coordinates['next'])
        if pinlabels:
            pyautogui.click(self.coordinates['pinlabels'])
        pyautogui.moveTo(position_after)

    def perform_save(self):
        pyautogui.click(self.coordinates['save'])

    def perform_collection(self, collection_name):
        self.write_with_clipboard(collection_name, 'collection')
        pyautogui.press('enter')

    def perform_collector(self, text_to_type):
        pyautogui.click(self.coordinates['collector_add'])
        self.write_with_clipboard(text_to_type, 'collector_name')
        pyautogui.press('enter')

    def perform_numbers_more(self, number, number_type):
        pyautogui.click(self.coordinates['numbers_more_button'])
        pyautogui.click(self.coordinates['numbers_more_number'])
        pyautogui.typewrite(str(number))
        self.write_with_clipboard(number_type, 'numbers_more_type')
        pyautogui.press('enter')

    def perform_date(self, text_to_type_verbatim, text_to_type_intrp):
        self.write_with_clipboard(text_to_type_verbatim, 'date_verbatim')
        self.write_with_clipboard(text_to_type_intrp, 'date_interpreted')

    def perform_taxon(self, taxon_name):
        self.write_with_clipboard(taxon_name, 'taxon')

    def perform_height(self, el_from, el_to):
        self.write_with_clipboard(el_from, 'elevation_from')
        self.write_with_clipboard(el_to, 'elevation_to')

    def perform_notes(self, text_to_type):
        self.write_with_clipboard(text_to_type, 'specimen_notes')

    def perform_sex(self, sex):
        self.write_with_clipboard(sex.capitalize(), 'sex')
        pyautogui.press('enter')

    def perform_workflow_status(self, status):
        self.write_with_clipboard(status, 'workflow_status')
        pyautogui.press('enter')

    def perform_determination(
        self,
        genus=None,
        species=None,
        subspecies=None,
        infraspecific=None,
        infrarank=None,
        author=None,
        determiner=None,
        date=None,
        verbatim=None
    ):
        pyautogui.click(self.coordinates['det_button'])
        pyautogui.click(self.coordinates['det_add_button'])

        if genus is not None:
            self.write_with_clipboard(genus, 'det_genus', clicks=2)

        if species is not None:
            self.write_with_clipboard(species, 'det_species', clicks=2)

        if subspecies is not None:
            self.write_with_clipboard(subspecies, 'det_subspecies', clicks=2)

        if infraspecific is not None:
            self.write_with_clipboard(infraspecific, 'det_infraspecific', clicks=2)

        if infrarank is not None:
            self.write_with_clipboard(infrarank, 'det_infrarank', clicks=2)

        if author is not None:
            self.write_with_clipboard(author, 'det_author', clicks=2)

        if determiner is not None:
            self.write_with_clipboard(determiner, 'det_determiner', clicks=2)

        if date is not None:
            self.write_with_clipboard(date, 'det_date', clicks=2)

        if verbatim is not None:
            self.write_with_clipboard(verbatim, 'det_verbatim', clicks=2)

        pyautogui.click(self.coordinates['det_done_button'])