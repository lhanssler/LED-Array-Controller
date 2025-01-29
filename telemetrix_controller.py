'''
This module is intended to control an LED array inside of a cryostat to be used for LED mapping of
an MKID wafer. The module should be run using an Arduino. While any Arduino should work, the
module was written using an Arduino Nano Every. This module uses the Telemetrix package to control
the Arduino over a serial connection, which requires a Telemetrix script to be run from the Arduino
IDE. Then, creating an instance of the Telemetrix class causes the program to locate the Arduino
board. This module also uses the telemetrix_pca9685 package to connect to all PCA9685 IC chips over
an I2C connection.

All connections are automatically set up when an instance of the Arduino class is created using a
configuration text file. The Arduino class's public methods should be sufficient for controlling
the LED array. In case more manual debugging is needed, the get_attributes method returns all
attributes of the Arduino object, including private attributes.

This module was created to be used with the LED Array Controller v3.0 PCB.

--------------
Written by Logan Hanssler, September 05 2024
University of Chicago South Pole Telescope Group
'''

import time
import numpy as np
from telemetrix.telemetrix import Telemetrix
from telemetrix_pca9685.telemetrix_pca9685 import TelemetrixPCA9685 as Driver

class Arduino:

    '''
    The Arduino object is intended to encapsulate the Arduino board itself as well as any
    Adafruit PCA9685 drivers hooked up to the board and the LED array which they are connected to.

    Attributes:
        __board (Telemetrix obj):  represents the Arduino board itself
        __drivers (1D array): contains all TelemetrixPCA9685 objects (Adafruit driver
                              representations) which were initialized along with the Arduino board
        __addresses (1D array): contains all addresses of the Adafruit drivers;
                                order in __addresses is the same as __drivers
        _LEDs (3D array): axes 0 and 1 are analogous to the LED array being controlled (axis 0 is
                          the row counting downward, axis 1 is the column counting left-to-right);
                          axis 2 is [cathode_pin, anode_channel, address]:
                              cathode_pin is the Arduino board's pin number which the LED uses as
                                  its cathode
                              anode_channel is the driver's channel number which the LED uses as
                                  its anode
                              address is the driver address corresponding to anode_channel

    Methods:
        __init__ (dunder): constructor
        __LED_array (private): helper method for the constructor
        _pin_mode (internal): directly changes an Arduino board pin to digital input,
                              digital output, or analog output mode
        _pin_out (internal): writes a digital output to an Arduino board pin;
                             assumes the specified pin is in digital output mode before the
                             method is called
        _channel_out (internal): writes a PWM output to a PCA9685 driver channel
        LED_on (public): turns a given LED on
        LED_blink (public): blinks a given LED on and off by calling LED_on and LED_off
        LED_off (public): turns a given LED off
        global_off (public): calls LED_off for every LED
        get_attributes (public): returns all attributes as a dictionary,
                                 including private attributes
    '''

    def __init__(self, file_path):
        '''
        Constructor method for the Arduino class.
        Calls __LED_array helper method to construct the LED array.
        Calls global_off method to reset the board and all drivers.

        Parameters:
            self
            file_path (str): file path for the configuration file which dictates the
                             LED array's setup;
                             required parameter, used to call __LED_array

        Returns:
            None
        '''
        # Reading out the config file
        config = np.loadtxt(file_path).astype(int)
        addresses = np.unique(config[:, 2])

        # Setting up private attributes
        self.__board = Telemetrix()
        self.__board.set_pin_mode_i2c()
        self.__addresses = addresses[np.where(addresses != 0)[0]]
        self.__drivers = np.array([Driver(board=self.__board,
                                          i2c_address=address) for address in self.__addresses])

        # Initializing the LED array
        self._LEDs = self.__LED_array(config)
        self.global_off()

    def __LED_array(self, config):
        '''
        Private helper method for the Arduino object's constructor.
        Called to create the _LEDs attribute from the configuration file's data.
        It is assumed that cathodes correspond to rows and use pins on the board, while
        anodes correspond to columns and use channels on a driver.

        Parameters:
            self
            config (2D array): result of np.loadtxt call on the configuration file;
                               data must be formatted as axis 0 distinguishing between different
                               pins/channels, axis 1 as [row_or_col_number, pin_or_channel_number,
                               driver_address];
                               a pin has no driver address, so driver_address should be
                               0 for a pin

        Returns:
            data (3D array): _LEDs attribute
        '''
        cathode_indices = np.where(config[:, 2] == 0)[0]
        anode_indices = np.where(config[:, 2] != 0)[0]
        cathodes = config[cathode_indices][:, :2] # No need for a blank address
        anodes = config[anode_indices]

        sorted_cathode_indices = np.argsort(cathodes[:, 0])
        sorted_anode_indices = np.argsort(anodes[:, 0])
        cathodes = cathodes[sorted_cathode_indices]
        anodes = anodes[sorted_anode_indices]

        num_rows, num_cols = np.max(cathodes[:, 0]), np.max(anodes[:, 0])
        pins, channels, addresses = np.zeros((3, num_rows, num_cols))

        pins += cathodes[:, 1][:, np.newaxis]
        channels += anodes[:, 1]
        addresses += anodes[:, 2]

        data = np.concatenate((pins[:, :, np.newaxis],
                               channels[:, :, np.newaxis],
                               addresses[:, :, np.newaxis]), axis=2)

        # Every time a pin_number's mode is updated, telemetrix tries to call
        # self.__board.digital_callbacks[pin_number]. This yields a warning if
        # pin_number is not a valid index; the next line prevents the warning.
        for pin in pins[:, 0]:
            self.__board.digital_callbacks[int(pin)] = None

        return data

    def _pin_mode(self, pin, mode):
        '''
        Directly changes an Arduino board pin to digital input, digital output, or analog output
        mode. These are equivalent to read, write, and pwm modes in the Arduino IDE.

        Parameters:
            self
            pin (int): pin number on the Arduino board whose mode should be changed
            mode (str): must either be 'READ', 'WRITE', or 'PWM':
                            'READ' calls set_pin_mode_digital_input
                            'WRITE' calls set_pin_mode_digital_output
                            'PWM' calls set_pin_mode_analog_output

        Returns:
            None
        '''
        if mode == 'READ':
            self.__board.set_pin_mode_digital_input(pin)
        elif mode == 'WRITE':
            self.__board.set_pin_mode_digital_output(pin)
        elif mode == 'PWM':
            self.__board.set_pin_mode_analog_output(pin)
        else:
            raise NameError('Invalid mode; mode must be \'READ\', \'WRITE\', or \'PWM\'')

    def _pin_out(self, pin, value):
        '''
        Writes a digital output to an Arduino board pin.
        Assumes the specified pin is in digital output mode before the method is called.

        Parameters:
            self
            pin (int): pin number on the Arduino board whose mode should be changed
            value (int): 1 for high voltage or 0 for low voltage

        Returns:
            None
        '''
        self.__board.digital_write(pin, value)

    def _channel_out(self, address, channel, on, off):
        '''
        Writes a PWM output to a PCA9685 driver channel.

        Parameters:

            self

            address (int): address of the driver whose channel should be written to

            channel (int): channel number being written to

            on (int): location in 4096-part cycle where the channel should be set to high;
                     must be between 0 and 4095, inclusive

            off (int): location in 4096-part cycle where the channel should be set to low;
                       must be between 0 and 4095, inclusive

        Returns:
            None
        '''
        driver = self.__drivers[np.where(self.__addresses == address)[0][0]]
        driver.set_pwm(channel, on, off)

    def LED_on(self, i, j=None, bright=1):
        '''
        Turns a given LED on by calling _pin_mode, _pin_out, and _channel_out methods for that
        LED's cathode pin and anode channel. Does not make assumptions about a pin or channel's
        state. Can either be called with an LED number or the LED's coordinates in the LED array.

        Parameters:
            self
            i (int): either the 0-indexed row coordinate of the desired LED,
                     or the desired LED's LED number;
                     LED numbers are 0-indexed and count from the upper left corner left-to-right
                     then downward (ex.: LED 6 in a 3x3 array is the rightmost LED in the
                     middle row)
            j (int): 0-indexed column coordinate of the desidred LED;
                     default value None should be maintained if i parameter is the LED number
            bright (iterable | float): if iterable, then [on, off] parameters for _channel_out();
                                       if float, then creates [on, off] parameters as
                                       [0,int(4095 * cycle)], so float must be between 0 and 1
                                       inclusive and describes LED brightness; default value 1
                                       corresponds to LED always on for max brightness

        Returns:
            None
        '''
        if j is None:
            # i refers to LED number
            num_cols = self._LEDs.shape[1]
            r = int(i / num_cols)
            c = i % num_cols
        else:
            # i, j are row, column
            r, c = i, j

        if not np.iterable(bright):
            bright = [0, int(4095 * bright)]

        LED = self._LEDs[r, c].astype(int)
        pin, channel, address = LED
        self._pin_mode(pin, 'WRITE')
        self._pin_out(pin, 0)
        self._channel_out(address, channel, *bright)

    def LED_off(self, i, j=None):
        '''
        Turns a given LED off by calling _pin_mode, _pin_out, and _channel_out methods for that
        LED's cathode pin and anode channel. Does not make assumptions about a pin or channel's
        state. Can either be called with an LED number or the LED's coordinates in the LED array.

        Parameters:
            self
            i (int): either the 0-indexed row coordinate of the desired LED,
                     or the desired LED's LED number;
                     LED numbers are 0-indexed and count from the upper left corner left-to-right
                     then downward (ex.: LED 6 in a 3x3 array -> rightmost LED in the middle row)
            j (int): 0-indexed column coordinate of the desidred LED;
                     default value None should be maintained if i parameter is the LED number

        Returns:
            None
        '''
        if j is None:
            # i refers to LED number
            num_cols = self._LEDs.shape[1]
            r = int(i / num_cols)
            c = i % num_cols
        else:
            # i, j are row, column
            r, c = i, j

        LED = self._LEDs[r, c].astype(int)
        pin, channel, address = LED
        self._channel_out(address, channel, 0, 0)
        self._pin_mode(pin, 'WRITE')
        self._pin_out(pin, 0)
        self._pin_mode(pin, 'READ')

    def global_off(self):
        '''
        Calls LED_off for every LED, thus never turning on any channels in their cycle and setting
        all pins to read mode with a write-ready low voltage.

        Parameters:
            self

        Returns:
            None
        '''
        num_rows, num_cols = self._LEDs.shape[0:2]
        num_LEDs = num_rows * num_cols
        for i in range(num_LEDs):
            self.LED_off(i)

    def LED_blink(self, i, j=None, num_iter=0, period=1, bright=1):
        '''
        'Blinks' a given LED by turning it on and off with a specified period for a
        specified number of iterations. Calls LED_on and LED_off to turn the LED on and off.

        Parameters:
            self
            i (int): i parameter for LED_on and LED_off
            j (int): j parameter for LED_on and LED_off
            num_iter (int): number of times to cycle the given LED;
                            1 cycle is defined as 1 iteration of turning the LED on then off;
                            default value 0 corresponds to no iterations
            period (float): total time length of 1 cycle in seconds;
                            the LED is turned on, then period / 2 seconds pass,
                            the LED is turned off, then period / 2 seconds pass again for a cycle;
                            default value 1 corresponds to turning the LED on for 0.5 second then
                            turning the LED off for 0.5 second
            bright (iterable | float): bright parameter for LED_on;
                                       default value 1 corresponds to turning the LED on at full
                                       brightness

        Returns:
            None                             
        '''
        for _ in range(num_iter):
            self.LED_on(i, j, bright)
            time.sleep(period / 2)
            self.LED_off(i, j)
            time.sleep(period / 2)

    def get_attributes(self):
        '''
        Returns all of self's attributes as a dictionary, including private attributes

        Parameters:
            self

        Returns:
            attributes (dict): keys are ['Board', 'Drivers', 'Addresses', 'LEDs'];
                               values are self's associated attributes
        '''
        attributes = {'Board': self.__board,
                      'Drivers': self.__drivers,
                      'Addresses': self.__addresses,
                      'LEDs': self._LEDs}
        return attributes
