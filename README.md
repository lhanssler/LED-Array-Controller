_________________________________
Instructions for using the package to control LEDs using an Arduino
_________________________________

**Part A: Installing Dependencies**
1. Download the Arduino IDE: https://www.arduino.cc/en/software
2. Open the IDE and select Tools/Manage Libraries
3. Search for Telemetrix4Arduino and install the library with dependencies
4. Clone the LED-Array-v3.0 repository
5. Move telemetrix, telemetrix_pca9685, and telemetrix_controller.py to the directory that Python searches for packages to import
6. Optional: The leftover files from LED-Array-v3.0 may be deleted at this point (README.md, example_config.txt, and the LED-Array-v3.0 directory)

**Part B: Running Code**
1. Connect the Arduino to the computer and select the Arduino's port in the Arduino IDE
2. Upload Telemetrix4Arduino to the Arduino by selecting File/Examples/Telemetrix4Arduino/Telemetrix4Arduino and clicking the Upload button in the IDE
3. telemetrix_controller should be imported into the Python file intending to control the LED array, and the module's docstrings can be referenced for use
