#!/bin/python

from gpiozero import LED, Button
from time import sleep

led = LED(2)
button = Button(14)

button.when_pressed = led.on
button.when_released = led.off

sleep(60)
