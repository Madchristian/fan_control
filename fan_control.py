#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time
import signal
import sys

# Set the BCM pin used to drive PWM fan
FAN_PIN = 18

# Set the PWM frequency in Hz
PWM_FREQ = 25

# Set the temperature thresholds and fan speeds
OFF_TEMP = 30
MIN_TEMP = 35
MAX_TEMP = 70
FAN_LOW = 1
FAN_HIGH = 100
FAN_OFF = 0
FAN_MAX = 100
FAN_GAIN = float(FAN_HIGH - FAN_LOW) / float(MAX_TEMP - MIN_TEMP)


def getCpuTemperature():
    with open('/sys/class/thermal/thermal_zone0/temp') as f:
        return float(f.read()) / 1000


def handleFanSpeed(fan, temperature):
    if temperature > MIN_TEMP:
        delta = min(temperature, MAX_TEMP) - MIN_TEMP
        fan.start(FAN_LOW + delta * FAN_GAIN)

    elif temperature < OFF_TEMP:
        fan.start(FAN_OFF)


# Set the GPIO mode explicitly
GPIO.setmode(GPIO.BCM)

# Create a PWM instance for the fan
fan = GPIO.PWM(FAN_PIN, PWM_FREQ)

# Set the initial fan speed to off
fan.start(FAN_OFF)

# Continuously monitor the temperature and adjust the fan speed
try:
    while True:
        temperature = getCpuTemperature()
        handleFanSpeed(fan, temperature)
        time.sleep(WAIT_TIME)

except KeyboardInterrupt:
    # Clean up the GPIO pins
    fan.stop()
    GPIO.cleanup()

except Exception as e:
    # Handle any other exceptions
    print('Error: %s' % e, file=sys.stderr)
    fan.stop()
    GPIO.cleanup()
    sys.exit(1)
