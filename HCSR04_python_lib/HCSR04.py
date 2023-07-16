# -*- coding:utf-8 -*-

from time import sleep, time
import RPi.GPIO as GPIO


class HCSR04:
    """
    A class to use the HC-SR04 ultrasonic distance sensor
    connected to the GPIO pins of a Raspberry Pi.
    """

    def __init__(self, trigger_pin: int = 18, echo_pin: int = 24):
        """
        Constructs all the necessary attributes for HCSR04 object.

        Args:
            trigger_pin: Pin for TRIGGER.
            echo_pin: Pin for ECHO.
        """

        self.TRIGGER_PIN = trigger_pin
        self.ECHO_PIN = echo_pin

    def check_connection(self) -> bool:
        """
        Checks that the ultrasonic distance sensor is connected.
        Based on the return of the echo pulse.

        Returns:
            connection: Sensor connection.
        """

        connection = False
        lost_counter = 0
        while lost_counter < 3:
            try:
                _ = self.get_distance(sample_size=1)
            except TimeoutError:
                lost_counter += 1
            except OSError:
                connection = True
                break
            else:
                connection = True
                break
        return connection

    def get_distance(self, sample_size: int = 3, decimal_places: int = 1) -> float:
        """
        Measures the distance from the sensor to an object in cm.
        The calculated distance is the median value of a sample of `sample_size` readings.

        Args:
            sample_size: Amount of distance readings.
            decimal_places: Number of decimal places for round.

        Raises:
            TimeoutError: if echo pulse was not received.
            OSError: if distance out of range 2-200 cm.

        Returns:
            distance_cm: Distance to an object in cm, rounded to one decimal place.
        """

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        # set GPIO directions (IN / OUT)
        GPIO.setup(self.TRIGGER_PIN, GPIO.OUT)
        GPIO.setup(self.ECHO_PIN, GPIO.IN)

        samples = []

        for i in range(sample_size):
            GPIO.output(self.TRIGGER_PIN, GPIO.LOW)
            sleep(0.05)
            # set Trigger to HIGH
            GPIO.output(self.TRIGGER_PIN, True)
            # set Trigger after 0.01ms to LOW
            sleep(0.00001)
            GPIO.output(self.TRIGGER_PIN, False)

            counter = 1
            start_time = time()
            arrival_time = time()

            while GPIO.input(self.ECHO_PIN) == 0:
                if counter < 10000:
                    start_time = time()
                    counter += 1
                else:
                    raise TimeoutError('Echo pulse was not received')

            while GPIO.input(self.ECHO_PIN) == 1:
                arrival_time = time()

            time_difference = arrival_time - start_time
            distance = (time_difference * 34300) / 2

            if 2 <= distance <= 200:
                samples.append(distance)
            else:
                raise OSError('Distance out of range 2-200 cm')

        # clean up only used pins to prevent clobbering any others in use
        GPIO.cleanup((self.TRIGGER_PIN, self.ECHO_PIN))
        sorted_samples = sorted(samples)
        median_sample = sorted_samples[sample_size // 2]
        distance_cm = round(median_sample, decimal_places)
        return distance_cm
