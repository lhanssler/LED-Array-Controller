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
4. warm_test.txt: A text file is used to configure the LED array controller
    when the telemetrix_controller.py module is utilized. This is the text
    file used for the January 2025 warm test in the LL113 cryostat and can be
    referenced as an example. The file is explained in more detail in Part C of
    the README.md.
5. serial # FILL THIS IN
6. KiCad Files # FILL THIS IN
7. README.md: This README file.

**Part B: Repository Dependencies**
1. Arduino IDE: Download at this link: https://www.arduino.cc/en/software
2. Telemetrix4Arduino, Arduino library: In the Arduino IDE,
    select Tools -> Manage Libraries and search for Telemetrix4Arduino.
    Install the library and its dependencies. The Telemetrix4Arduino example
    file should be flashed to the Arduino to connect to Python code.
3. telemetrix, telemetrix_pca9685, serial: Python packages included in this
    repository which are dependencies of the telemetrix_controller.py file.
4. Configuration text file: # FILL THIS IN

**Part C: Instructions for Using telemetrix_controller**
1. txt file # FILL THIS IN
2. code stuff # FILL THIS IN

Prior text:
1. Connect the Arduino to the computer and select the Arduino's port in the Arduino IDE
2. Upload Telemetrix4Arduino to the Arduino by selecting File/Examples/Telemetrix4Arduino/Telemetrix4Arduino and clicking the Upload button in the IDE
3. telemetrix_controller should be imported into the Python file intending to control the LED array, and the module's docstrings can be referenced for use
