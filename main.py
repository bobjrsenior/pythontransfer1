#!/bin/python

from gpiozero import LED, Button
from time import sleep
from pydub import AudioSegment
from pydub.playback import play

led = LED(2)
button = Button(14)

button.when_pressed = led.on
button.when_released = led.off

song = AudioSegment.from_wav("audio/woah.wav")
play(song)

sleep(60)
