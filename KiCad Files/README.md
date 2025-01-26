The KiCad Files folder contains the two most recent revisions of the LED Array
PCB (LAP): v3.0 and v4.0.

The telemetrix_controller module was designed with v3.0 in mind, and v3.0 is
the version that is printed and populated in LL113. v3.0 contains:
- An Arduino Nano (used with header pins), PCA9685 IC which is SMT soldered
    directly to the board.
- A through-hole D-sub 37 connector to connect to the LED array in the
    cryostat.
- Through-hole resistors for each anode.
- Through-holes which can be used to add capacitors to GND in parallel with
    the LED array anodes.
- Unconnected solder jumpers which can be used to assign an address to
    the board's PCA9685.
- Two through-hole connections each for VCC, GND, OE, SDA, and SCL lines,
    which allow multiple copies of the PCB to be daisy-chained for using
    multiple drivers (this requires each board to have a different address,
    as indicated through connecting solder jumpers).
- Pulldown resistors and an indicator LED.

There is one potential issue with v3.0: the RX and TX pins on the Arduino Nano
are routed to the D-sub 37 connector, which implies that they can be used as
cathodes. This is not possible, as these are the RX and TX lines that are used
by the USB connection between the Arduino and host device, so they cannot be
used for the LED array.
Issues can be avoided by simply not connecting these D-sub 37 connector pins to
the LED array. v4.0 avoids any confusion by not routing the TX or RX pins to the
D-sub 37 connector. In addition to the TX and RX routing improvement, v4.0 also
uses SMT resistors instead of through-hole resistors, resulting in a reduced PCB
size. v3.0 and v4.0 are otherwise the same.
