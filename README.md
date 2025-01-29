**LED-Array-Controller**

**Part A: Repository Contents**
1. telemetrix_controller.py: Python module created to interact with the Arduino
    Nano. Allows the Nano to connect to a PCA9685 driver and flash LEDs.
    This module is the only required import. Other files are dependencies.
2. telemetrix: Python package which can be imported to control an Arduino
    using Python over a serial connection. This package is a dependency of
    telemetrix_controller.py and telemetrix_pca9685.
3. telemetrix_pca9685: Python package which can be imported to connect with an
    Arduino and PCA9685 driver. The package uses telemetrix for the Arduino
    connection and is a dependency of telemetrix_controller.py. The package
    was sourced from: https://github.com/MrYsLab/telemetrix-extensions
4. Telemetrix4Arduino: Folder containing Telemetrix4Arduino.ino, the Arduino
    sketch file which must be opened in the Arduino IDE and uploaded to the
    Arduino Nano before the connection from Python is established. ino files
    can only be opened in the Arduino IDE if they are located in a folder
    of the same name, which is why the folder is provided.
5. warm_test.txt: A text file is used to configure the LED array controller
    when the telemetrix_controller.py module is utilized. This is the text
    file used for the January 2025 warm test in the LL130 cryostat and can be
    referenced as an example. The file is explained in more detail in Part C of
    the README.md.
6. serial: Python's serial library, a dependency of telemetrix. serial is
    should already be installed on the host device, but some devices running
    older versions of Python have issues when telemetrix calls certain functions
    from serial. This version of serial has been shown to function properly.
7. KiCad Files: Folder containing the KiCad files for LED Array Controller PCBs.
    Revisions 3 and 4 of the board are in the folder, which includes their
    schematics and board diagrams. KiCad Files has its own README file in
    the folder.
8. README.md: This README file.

**Part B: Repository Dependencies**
1. Arduino IDE: Download at this link: https://www.arduino.cc/en/software
2. Telemetrix4Arduino: Arduino library. Download instructions:
    In the Arduino IDE, select Tools -> Manage Libraries and search for
    Telemetrix4Arduino. Install the library and its dependencies.
3. Telemetrix4Arduino.ino, Arduino sketch: File to be uploaded to the Arduino
    Nano to begin the serial connection. This is the Telemetrix4Arduino library
    example file.
4. telemetrix, telemetrix_pca9685, serial: Python packages included in this
    repository which are dependencies of the telemetrix_controller.py file.
5. Configuration text file: The text file which defines the LED Array PCB's
    connection to the LED Array Controller PCB.

**Part C: Instructions for Using telemetrix_controller**
1. Create the configuration file: This is the text file, with warm_test.txt as
    an example. Each row represents an Arduino Nano pin or PCA9685 driver
    channel to be used for the LED array. Each row has 3 columns delimited by a
    single space. The first column is the row or column number (1-indexed) of
    the LED array which the pin/channel corresponds to. The second column is
    the digital pin or channel number. The third number is the driver address.
    If the text row corresponds to a Nano pin, then the driver address should
    be entered as 0. The default driver address is 64 (or 0x40), which
    corresponds to none of the solder jumpers being connected on the LED Array
    Controller PCB.
2. In the Arduino IDE, upload the Telemetrix4Arduino.ino file to the Arduino
    Nano.
3. In Python, import telemetrix_controller. No other explicit imports are
    required for repository use.
4. In Python, create an object from the telemetrix_controller.Arduino class. The
    constructor only has one argument, which is required: the string indicating
    the filepath to the configuration file.
5. The object's methods can now be called to control the LED array.
    Please refer to the docstrings in telemetrix_controller.py for further
    instructions on use.