import random
import random
import re
import time
import tkinter as tk

import keyboard
import mouse
import numpy as np
from PIL import ImageGrab
from PIL.ImImagePlugin import number
from setuptools.config.setupcfg import configuration_to_dict

from utils import *

custom_config = r'--oem 3 --psm 6 outputbase digits'

# Determine screen coordinates
verbose = True

COORDINATES['tag_approximate'] = (COORDINATES['pinlabels'][0]+250, COORDINATES['pinlabels'][1]+260)

if verbose:
    print("Coordinates:")
    for k, v in COORDINATES.items():
        print(f'{k}: {v}')
    print('-' * 40)

def clean_text(text):
    # Step 1: Remove all non-numeric characters except for "("
    cleaned_text = re.sub(r'[^0-9(]', '', text)

    # Check if the cleaned text is not empty
    if not cleaned_text:
        return None  # Return None for invalid input

    # Step 2: If the number contains 5 digits and starts with "(", convert "(" to "1"
    if len(cleaned_text) == 5 and cleaned_text.startswith('('):
        cleaned_text = '1' + cleaned_text[1:]

    # Step 3: If the number contains 6 digits and starts with "1", remove the "1"
    if len(cleaned_text) == 6:
        cleaned_text = cleaned_text[1:]

    # Step 4: If the number contains 5 digits and starts with "8", convert "8" to "3"
    if len(cleaned_text) == 5 and cleaned_text.startswith('8'):
        cleaned_text = '3' + cleaned_text[1:]

    # Convert to integer and ensure it is within the range 1 to 63000
    try:
        number = int(cleaned_text)
        if 1 <= number <= 63000:
            return number
        else:
            return None  # Return None for out-of-range numbers
    except ValueError:
        return None  # Return None for conversion failures

def perform_ocr(position=None, width=200, height=80, jitter_size=15, min_samples=None, num_samples=5, verbose = False):
    """
    Capture a screen area around the given position, apply OCR, and return the most common valid result.

    Parameters
    ----------
    position : tuple, optional
        The center point for capturing the screen (default: current mouse position).
    width : int, optional
        Width of the capture area.
    height : int, optional
        Height of the capture area.
    jitter_size : int, optional
        The jitter range around the position.
    min_samples : int, optional
        Minimum number of valid samples to consider.
    num_samples : int, optional
        Number of jittered samples to take.
    verbose : bool, optional
        Whether to print debug information

    Returns
    -------
    str or None
        Most common OCR result from the sampled screenshots.
    """

    if position is None:
        # Get the current cursor position
        position = pyautogui.position()

    x, y = position
    if verbose:
        print(f"Capturing around position: {x}, {y}")

    if min_samples is None:
        min_samples = num_samples

    # List to store OCR results
    ocr_results = []
    valid_results = []

    print('-' * 40)

    for _ in range(num_samples):  # Take the specified number of samples
        jitter_x = random.randint(-jitter_size, jitter_size)
        jitter_y = random.randint(-jitter_size, jitter_size)

        # Define the capture area around the jittered position
        top_left_x = x + jitter_x - (width // 2)
        top_left_y = y + jitter_y - (height // 2)
        bottom_right_x = top_left_x + width
        bottom_right_y = top_left_y + height

        if verbose:
            print(f"Capturing area from {top_left_x, top_left_y} to {bottom_right_x, bottom_right_y}")

        # Capture the screenshot of the specified area
        screenshot = ImageGrab.grab(bbox=(top_left_x, top_left_y, bottom_right_x, bottom_right_y))

        # Perform OCR on the captured image
        text = pytesseract.image_to_string(screenshot, config=custom_config)

        # Clean the text
        cleaned_text = clean_text(text)

        # Store the cleaned OCR result
        ocr_results.append(cleaned_text)

        if cleaned_text is not None:
            valid_results.append(cleaned_text)

        print(cleaned_text)
        if valid_results and len(valid_results) >= min_samples and len(set(valid_results)) == 1:
            break

    # Determine the most frequent valid result
    if valid_results:
        most_common_result = max(set(valid_results), key=valid_results.count)
        pyperclip.copy(str(most_common_result))  # Copy to clipboard
        print('-' * 40)
        print(most_common_result)
        return most_common_result
    else:
        print("No valid OCR results found.")
        return None


def locate_and_average_centers(tags_folder='imgs/tags/digits', confidence=0.5, verbose=True):
    # Initialize an empty list to hold the found centers
    found_centers = []

    # Get all files in the tags folder
    tag_images = [f for f in os.listdir(tags_folder) if f.endswith(('.png', '.jpg', '.jpeg', '.PNG', '.JPG', '.JPEG'))]
    if verbose:
        print(tag_images)

    # Iterate over the tag images
    for image_file in tag_images:
        image_path = os.path.join(tags_folder, image_file)

        if verbose:
            print(f"Searching for: {image_path}")

        try:
            # Locate the center of the current tag on the screen
            center = pyautogui.locateCenterOnScreen(image_path, confidence=confidence)

            if center is not None:
                found_centers.append(center)
                if verbose:
                    print(f"Found {image_path} at: {center}")
            else:
                if verbose:
                    print(f"{image_path} not found on the screen.")

        except pyautogui.ImageNotFoundException:
            if verbose:
                print(f"Image file {image_path} not found. Skipping...")

    # Calculate the average of the found centers if any
    if found_centers:
        # Convert to numpy array for easier manipulation
        centers_array = np.array(found_centers)

        # Calculate the center x-coordinate
        min_x = np.min(centers_array[:, 0])
        max_x = np.max(centers_array[:, 0])
        center_x = (min_x + max_x) / 2

        # Calculate the average y-coordinate
        average_y = np.mean(centers_array[:, 1])

        return center_x, average_y  # Return as a tuple
    else:
        if verbose:
            print("No tags found.")
        return None

def show_input_dialog():
    # Create a new Tkinter window
    root = tk.Tk()
    root.title("Input Box")

    # Set the size of the window
    window_width = 600
    window_height = 200

    # Calculate the position to center the window on the screen
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)

    # Set the geometry of the window
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")
    root.attributes("-topmost", True)  # Keep the window on top

    # Function to handle the OK button click
    def on_ok(event=None):  # Allow passing an event for Enter key
        user_input = entry.get()  # Get the input from the entry box
        cleaned_user_input = clean_text(user_input)  # Clean and validate the input
        pyperclip.copy(cleaned_user_input)  # Copy to clipboard
        print("Copied to clipboard:", cleaned_user_input)  # Optional: Print to console
        root.destroy()  # Close the window
        perform_paul_born()

    # Create and place a label
    label = tk.Label(root, text="Enter your text:", font=("Arial", 18))
    label.pack(pady=10)

    # Create and place a larger entry box
    entry = tk.Entry(root, width=50, font=("Arial", 18))
    entry.pack(pady=5)

    # Bind the Enter key to the on_ok function
    entry.bind('<Return>', on_ok)  # Bind Enter key to OK action

    # Create and place a larger OK button
    ok_button = tk.Button(root, text="OK", command=on_ok, font=("Arial", 18))
    ok_button.pack(pady=10)

    # Run the Tkinter main loop
    root.update()  # Update the window to ensure it is rendered
    root.after(0, lambda: pyautogui.click(entry.winfo_rootx() + 10, entry.winfo_rooty() + 10))  # Click in the entry box

    root.mainloop()

def perform_paul_born():
    # Perform the actions for Paul Born
    number = pyperclip.paste()
    perform_actions_numbers_more(number, "Collection Number")
    perform_actions_collection("Born-Moser, Paul (1859-1928)")
    perform_save()

def perform_auto_locate_ocr(confidence=0.5, verbose=True):
    center = locate_and_average_centers(confidence=confidence, verbose=verbose)
    if center is not None:
        perform_ocr(center, 200, 80, 15, 3, 5)
    else:
        print("No tag found.")


# HOTKEYS
keyboard.add_hotkey('alt+2', perform_previous, args=(COORDINATES['tag_approximate'], True))
keyboard.add_hotkey('alt+1', perform_next, args=(COORDINATES['tag_approximate'], True))
keyboard.add_hotkey('§', perform_paul_born)
keyboard.add_hotkey('alt+§', show_input_dialog)  # New hotkey for manual number input
keyboard.add_hotkey('alt+q', perform_auto_locate_ocr)

mouse.on_middle_click(perform_ocr, args=(None, 200, 80, 15, 3, 5))

while True:
    keyboard.wait()

