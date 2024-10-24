import keyboard

from utils import *

# Determine screen coordinates, set add_determination=True if you want to automate determination entries
SA = ScreenAutomation(add_determination=True, verbose=True)

def perform_combined_example_action():
    """
    This function demonstrates how to combine multiple actions into a single function.

    Let's say you want to perform the following actions:
    1. Click the 'Collection' button
    2. Type the collection name 'Weber, Paul (1881-1968)'
    3. Click the 'Add Collector' button
    4. Type the collector name 'Weber, Paul (1881-1968)'
    5. Click the 'Numbers More' button
    6. Type the number '12093' and select 'Collection Number'
    7. Type the date 'V.1934' and '1934/05'
    8. Type the taxon name 'Laboulbenia (Baumgartner)'
    9. Type the height '350' and '400'
    10. Type the notes 'Pink dot\n'
    11. Save the changes

    This function combines all the above actions into a single function and allows you to perform them with a single hotkey.
    """

    # Fill in the collection name
    SA.perform_collection("Weber, Paul (1881-1968)")
    # Fill in the collector name
    SA.perform_collector("Weber, Paul (1881-1968)")
    # Fill in the numbers & more
    SA.perform_numbers_more(12093, 'Collection Number')
    # Fill in the date (verbatim & interpreted (yyyy/mm/dd))
    SA.perform_date("V.1934", "1934/05")
    # Fill in the specimen notes
    SA.perform_notes("Pink dot\n")

    # Save the changes
    SA.perform_save()

def paul_born_collection_collector():
    SA.perform_collection("Weber, Paul (1881-1968)")
    SA.perform_collector("Weber, Paul (1881-1968)")
    SA.perform_save()

def perform_determination1():
    SA.perform_determination(
        genus="Sunira",
        species="circellaris",
        subspecies=None,
        infraspecific=None,
        infrarank=None,
        author="H.",
        determiner="H-U. Grunder",
        date="1985",
        verbatim="9978"
    )
    SA.perform_save()

# --------------------------------------------------
# HOTKEYS
keyboard.add_hotkey('alt+left', SA.perform_previous)
keyboard.add_hotkey('alt+right', SA.perform_next)

keyboard.add_hotkey('ctrl+p', perform_combined_example_action)

keyboard.add_hotkey('ctrl+g', perform_determination1)

# --------------------------------------------------
# HOTKEY EXAMPLES
# To activate a hotkey, uncomment the corresponding line (remove the '#' at the beginning of the line)

# Hotkeys to fill in the collection and collector name
# keyboard.add_hotkey('ctrl+p', SA.perform_actions_collection, args=["Weber, Paul (1881-1968)"])
# keyboard.add_hotkey('ctrl+o', SA.perform_actions_collector, args=["Weber, Paul (1881-1968)"])

# keyboard.add_hotkey('ctrl+b', SA.perform_actions_collection, args=["Birchler, Alfons (1905-1983)"])
# keyboard.add_hotkey('ctrl+n', SA.perform_actions_collector, args=["Birchler, Alfons (1905-1983)"])

# Hotkey to perform the 'previous' action
# keyboard.add_hotkey('alt+left', SA.perform_previous)

# Hotkey to perform the 'next' action
# keyboard.add_hotkey('alt+right', SA.perform_next)

# Hotkey to perform the 'save' action
# keyboard.add_hotkey('ctrl+s', SA.perform_save)

# Hotkey to perform the 'collection' action with a specific collection name
# keyboard.add_hotkey('alt+p', SA.perform_actions_collection, args=["Weber, Paul (1881-1968)"])

# Hotkey to perform the 'collector' action with a specific text
# keyboard.add_hotkey('alt+o', SA.perform_actions_collector, args=["Weber, Paul (1881-1968)"])

# Hotkey to perform the 'numbers more' action with a specific number and type
# keyboard.add_hotkey('alt+n', SA.perform_actions_numbers_more, args=[12093, 'Collection Number'])

# Hotkey to perform the 'date' action with specific verbatim and interpreted dates
# keyboard.add_hotkey('ctrl+d', SA.perform_actions_date, args=["V.1934", "1934/05"])

# Hotkey to perform the 'taxon' action with a specific taxon name
# keyboard.add_hotkey('ctrl+t', SA.perform_actions_taxon, args=["Laboulbenia (Baumgartner)"])

# Hotkey to perform the 'height' action with specific elevation from and to values
# keyboard.add_hotkey('ctrl+h', SA.perform_actions_height, args=["340", "340"])

# Hotkey to perform the 'notes' action with specific text
# keyboard.add_hotkey('ctrl+n', SA.perform_actions_notes, args=["Pink dot\n"])

# Hotkey to perform the 'sex' action with a specific sex
# keyboard.add_hotkey('ctrl+x', SA.perform_actions_sex, args=["male"])

# Hotkey to perform the 'workflow status' action with a specific status
# keyboard.add_hotkey('ctrl+w', SA.perform_actions_workflow_status, args=["Specialist Reviewed"])


# Main loop
while True:
    keyboard.wait()