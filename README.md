# Paul Born OCR Project

Welcome to the **PaulBornOCR** project! This document provides comprehensive installation and setup instructions to help you get started with the project. 

**Author**: Dustin Brunner (brunnedu@ethz.ch)

The purpose of this document is to guide users through the necessary prerequisites, setup instructions, and usage of the `paul_born_ocr.py` script. This project utilizes Optical Character Recognition (OCR) to automate data entry processes, streamlining your workflow.

## Table of Contents

1. [Prerequisites](#prerequisites)
   - [Install PyCharm Community Edition](#1-install-pycharm-community-edition)
   - [Install Tesseract](#2-install-tesseract)
   - [Install Miniconda](#3-install-miniconda)
2. [Setup Instructions](#setup-instructions)
   - [Create the Conda Environment](#1-create-the-conda-environment)
   - [Configure PyCharm](#2-configure-pycharm)
3. [Using the `paul_born_ocr.py` Script](#using-the-paul_born_ocrpy-script)
   - [Run the Script](#run-the-script)
   - [Checking Coordinates](#checking-coordinates)
   - [Shortcuts](#shortcuts)
4. [Important Notes](#important-notes)
5. [Troubleshooting](#troubleshooting)
   - [Common Issues](#common-issues)
   - [Additional Support](#additional-support)



### Prerequisites

Before proceeding with the setup, ensure that you have the following files in a folder named **`PaulBornOCR`** located in your **Downloads** directory:

- `environment.yml`
- `utils.py`
- `paul_born_ocr.py`
- `imgs/`

You can download these files from the GitHub repository or from the **Born-Moser, Paul** directory on the **Google Drive** of the entomological collection.
### 1. Install PyCharm Community Edition
PyCharm is an Integrated Development Environment (IDE) that makes it easier to manage your Python projects. Download and install **PyCharm Community Edition** from the official JetBrains website:

- **Download URL**: [PyCharm Community Edition](https://www.jetbrains.com/pycharm/download/)

#### Steps:
1. Run the installer.
2. Follow the on-screen instructions to complete the installation.
3. During installation, you may want to select options such as:
   - Add PyCharm to the system PATH.
   - Create a desktop shortcut for easy access.

### 2. Install Tesseract
Tesseract is an open-source OCR engine that `pytesseract` relies on. You need to install it and make sure it is available in the default path.

#### Steps:
1. Download the Tesseract installer from the official GitHub page:
   - **Download URL**: [Tesseract OCR Installer](https://github.com/UB-Mannheim/tesseract/wiki)
2. Run the installer and select the default installation options. Tesseract should be installed in the following directory:
   - `C:\Users\<YourUsername>\AppData\Local\Programs\Tesseract-OCR\tesseract.exe`

### 3. Install Miniconda
Miniconda is a lightweight version of Anaconda that lets you manage Python environments and packages.

#### Steps:
1. Download Miniconda from the official website:
   - **Download URL**: [Miniconda Installer](https://docs.conda.io/en/latest/miniconda.html)
2. Run the installer and select the default installation options. Miniconda should be installed in the following directory:
   - `C:\Users\<YourUsername>\AppData\Local\miniconda3`
3. Once installed, open the **Anaconda Prompt (miniconda3)** from the Windows Start Menu and verify the installation by typing:
   ```bash
   conda --version
    ```
    You should see the version number of Miniconda displayed in the console.

## Setup Instructions

### 1. Create the Conda Environment

1. Open the **Anaconda Prompt (miniconda3)** from the Windows Start Menu.
2. Navigate to the project directory containing the `environment.yml` file:

    ```bash
    cd Users\<YourUsername>\Downloads\PaulBornOCR
    ```

3. Create the environment using the following command:

    ```bash
    conda env create -f environment.yml
    ```

    This will create a Conda environment named `data_entry_shortcuts` with the necessary dependencies.


### 2. Configure PyCharm

1. **Open PyCharm and Access Settings**:  
   Launch PyCharm and open your project. Press **Ctrl + Alt + S** (Windows/Linux) or **Cmd + ,** (macOS) to open **Settings**. Alternatively, click the gear icon in the bottom-right corner.

2. **Navigate to Python Interpreter**:  
   In **Settings**, select **Project: <Your Project Name>** from the left sidebar, then click on **Python Interpreter**. Click **Add Interpreter** in the top-right corner.

3. **Select Conda Environment**:  
   - In the **Add Python Interpreter** window, choose **Conda Environment** and select **Existing environment**.  
   - Click the folder icon to browse for the Conda executable, navigating to:  
     `C:\Users\<Your Username>\AppData\Local\miniconda3\Scripts\conda.exe`  
     (replace `<Your Username>` with your actual username).  
   - PyCharm will automatically load your Conda environments. Wait for the list to appear.

4. **Select and Apply Changes**:  
   From the loaded environments, select `data_entry_shortcuts`, then click **OK**. Ensure it’s selected in the Python Interpreter settings, then click **Apply** and **OK** to save changes.

5. **Verify Configuration**:  
   Check the bottom-right corner of PyCharm to confirm that the selected interpreter is active.

## Using the `paul_born_ocr.py` Script

### Run the Script
1. Open the **Data Shot** software and load a specimen for data entry.
2. Run the `paul_born_ocr.py` script from PyCharm by clicking **Run > Run 'paul_born_ocr'** or using **Shift + F10**.
3. The script will detect on-screen elements and automate the data entry process.

### Checking Coordinates
After running the script, check the console output to verify that all necessary screen coordinates were detected. If a screen element is missing, ensure that:
- The element is visible and properly loaded on your screen.
- The main monitor (where your Windows login appears) is used.

### Shortcuts

The script provides several keyboard shortcuts for quickly navigating and entering data in the **Data Shot** software:

- **Alt + 1**: Move to the next specimen and zoom in on the pin labels.
- **Alt + 2**: Move to the previous specimen and zoom in on the pin labels.
- **Middle Mouse Click**: Automatically recognize the number on the Paul Born collection number label and copy it to the clipboard. (Ensure that the mouse is centered on the number before clicking.)
- **§ (Section Key)**: Fill in the collection number from the clipboard and set the collection to "Born-Moser, Paul."
- **Alt + §**: Show an input dialog for manual collection number entry if automatic recognition did not work.
- **Alt + Q**: Automatically detect the position of the collection number on the screen. (This feature works about 50% of the time and is likely slower than moving the mouse to the collection number and clicking the middle mouse button.)

## Important Notes
- Ensure that **Data Shot** is open on your primary monitor (the one where the Windows login screen appears). The script relies on screen coordinates and can fail if Data Shot is opened on a different monitor.
- When running the OCR, verify that the correct data is captured, especially for numbers and labels, as OCR accuracy can vary depending on the clarity of the screen content.
- You may need to adjust your screen layout or resolution to ensure all elements are detected properly.


## Troubleshooting

If you encounter issues while setting up or running the `PaulBornOCR` project, consider the following solutions:

### Common Issues

1. **PyCharm Fails to Detect Conda Environment**:
   - Ensure that you have correctly installed Miniconda and that the path to `conda.exe` is accurate. Double-check the directory:  
     `C:\Users\<Your Username>\AppData\Local\miniconda3\Scripts\conda.exe`.
   - Restart PyCharm after installation to refresh the environment list.

2. **Tesseract Installation Problems**:
   - If the Tesseract OCR engine is not found, verify that Tesseract is installed in the specified directory and that its path is included in your system’s environment variables.
   - You can add the Tesseract installation path to your PATH variable by following these steps:
     - Right-click on **This PC** or **My Computer** and select **Properties**.
     - Click on **Advanced system settings** and then **Environment Variables**.
     - In the **System variables** section, find and select the **Path** variable, then click **Edit**.
     - Add the Tesseract installation path:  
       `C:\Users\<YourUsername>\AppData\Local\Programs\Tesseract-OCR\`.

3. **OCR Not Detecting Elements on the Screen**:
   - Make sure that the **Data Shot** software is open on your primary monitor. The script relies on screen coordinates and may not function correctly if it is displayed on a different monitor.
   - Check that the elements are visible and clearly loaded on the screen. Adjust your screen resolution if necessary.

4. **Script Throws Errors or Fails to Run**:
   - Ensure that all dependencies in the `environment.yml` file are installed correctly. You can try recreating the environment using:  
     ```bash
     conda env remove -n data_entry_shortcuts
     conda env create -f environment.yml
     ```

### Additional Support

If you need more detailed instructions on any of the steps or encounter a unique issue not covered here, consider using ChatGPT. You can ask specific questions about your setup, error messages, or any part of the process that is difficult to understand. ChatGPT can provide tailored guidance and troubleshooting tips to help you resolve your issues.

