#!/bin/python

from gpiozero import LED, Button
from time import sleep
from playsound import playsound

led = LED(2)
button = Button(14)

button.when_pressed = led.on
button.when_released = led.off

playsound('audio/woahh.ogg')

sleep(60)
