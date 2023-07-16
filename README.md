# HC-SR04 Python Library for Raspberry Pi
**Author:** Jakub Przepiórka \
**Version:** 0.0.1


## About
Library for HC-SR04 ultrasonic distance sensor used with Raspberry Pi.

**Operating system** \
Library is dedicated to use on Raspberry Pi OS.


## How does it work
To start the measurement, a voltage pulse (5V high state) is provided to the TRIG pin for 10 us.
The module measures the distance using a sound wave with a frequency of 40 kHz.
A signal is sent to the microcontroller, where the distance can be calculated based on the duration
of the high state using the formula below:

**measured distance = (high level time × 34300 / 2**

Duration of the high state is multiplied with the sonic speed in the air (34300 cm/s) and
divided by 2 (because there and back).

The calculated distance is the median of distance readings.


## Installation
**Note**: Python GPIO library should be installed.

The preferred channel to install this library is [PyPI](https://pypi.org/project/HCSR04_python_lib/):
```
pip3 install HCSR04_python_lib
```

Alternatively, you can clone [project repository](https://github.com/JakubPrz/HCSR04_python_lib):
```
git clone git@github.com:JakubPrz/HCSR04_python_lib.git
```


## Example
```python
from HCSR04_python_lib import HCSR04
from time import sleep


hcsr_sensor = HCSR04(trigger_pin=18, echo_pin=24)

try:
    while True:
        distance = hcsr_sensor.get_distance(sample_size=5, decimal_places=2)
        print(f'Distance = {str(distance)} [cm]')
        sleep(0.5)

except TimeoutError as ex:
    print(f'ERROR getting distance: {ex}')

except OSError as ex:
    print(f'ERROR getting distance: {ex}')

except KeyboardInterrupt:
    print('Measurement stopped.')
```


## Error management
```TimeoutError``` - Echo pulse was not received, because the sensor is not connected.

```OSError``` - Distance out of range 2-200 cm. Maybe try measure distance again?


## Contributing
Contributions are welcome! \
If you would like to make any improvements to this library, feel free to submit a pull request.


## License
This project is licensed under the MIT License - see the LICENSE.md file for details.