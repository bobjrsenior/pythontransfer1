#!/bin/python

from gpiozero import LED, BUTTON
from gpiozero import 
from time import sleep

led = LED(2)
button = BUTTON(14)

button.when_pressed = led.on
button.when_released = led.off

sleep(60)
