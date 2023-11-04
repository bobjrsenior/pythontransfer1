#!/bin/python

from gpiozero import LED, Button
from time import sleep
from pydub import AudioSegment
from pydub.playback import _play_with_simpleaudio

led = LED(2)
button = Button(14)

button.when_pressed = led.on
button.when_released = led.off

song = AudioSegment.from_ogg("audio/woah.ogg")
_play_with_simpleaudio(song)

sleep(60)
