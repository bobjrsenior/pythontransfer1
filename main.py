#!/bin/python

from gpiozero import LED, Button
from time import sleep
from pydub import AudioSegment
from pydub.playback import play
import random
import time

step_time = 2000
#actions = {"LEFT", "MIDDLE", "RIGHT", "WIRES"}
actions = {"LEFT"}
current_action = None
won = False
lost = False
completed_action = True
completed_actions = -1
step_start = 0

led = LED(2)
left_button = Button(14)

def get_clip(action):
    return AudioSegment.from_ogg("audio/woah.ogg")

def play_sound(action):
    play(get_clip(action))

def get_time():
    return time.time_ns() * 1000 * 1000

def button_left_pressed():
    led.on
    if current_action == "LEFT":
        completed_action = True
        print("COMPLETED ACTION")

def button_left_released():
    led.off



left_button.when_pressed = button_left_pressed
left_button.when_released = button_left_released

song = AudioSegment.from_ogg("audio/woah.ogg")
play(song)

while not lost and not won:
    if completed_action:
        completed_actions += 1
        current_action = random.choice(actions)
        competed_action = False
        play_sound(current_action)
        step_time = int(step_time * 0.95)
        step_start = get_time()
    elif get_time() > step_start + step_time:
        print("LOST")
        lost = True

print("GAME_COMPLETED")
sleep(60)
