#!/bin/python

from gpiozero import LED, Button
from time import sleep
from pydub import AudioSegment
from pydub.playback import play
import random
import time


LEFT_BUTTON_LED = 14
MIDDLE_BUTTON_LED = 23
RIGHT_BUTTON_LED = 16
WIRES_BUTTON_LED = 21

UV_LED = 5
LEFT_RED_LED = 17
RIGHT_RED_LED = 6
GREEN_LED = 10

current_win_count = 0
button_presses_to_win = 20

save_filename = "wins.txt"

with open("wins.txt", "r") as file:
    current_win_count = int(file.read())
    
button_presses_to_win += current_win_count * 2
step_time = 20000
actions = ["LEFT", "MIDDLE", "RIGHT", "WIRES"]
#actions = ["WIRES"]
current_action = None
won = False
lost = False
completed_action = True
completed_actions = -1
left_button_pressed = False
right_button_pressed = False
middle_button_pressed = False
wires_button_pressed = False


step_start = 0

left_audio = AudioSegment.from_file("audio/Left.wav", format="wav")
middle_audio = AudioSegment.from_file("audio/Middle.wav", format="wav")
right_audio = AudioSegment.from_file("audio/Right.wav", format="wav")
wires_audio = AudioSegment.from_file("audio/Wires.wav", format="wav")


#led = LED(2)
left_button = Button(LEFT_BUTTON_LED, bounce_time=0.05)
middle_button = Button(MIDDLE_BUTTON_LED, bounce_time=0.05)
right_button = Button(RIGHT_BUTTON_LED, bounce_time=0.05)
wires_button = Button(WIRES_BUTTON_LED, bounce_time=0.05)

uv_led = LED(UV_LED)
left_red_led = LED(LEFT_RED_LED)
right_red_led = LED(RIGHT_RED_LED)
green_led = LED(GREEN_LED)



def get_lose_haiku():
    haiku = ["Lose_Haiku_1.wav", "Lose_Haiku_2.wav"]
    return AudioSegment.from_file("audio/" + random.choice(haiku), format="wav")

def get_win_haiku():
    haiku = ["Win_Haiku_1.wav", "Win_Haiku_2.wav", "Win_Haiku_3.wav"]
    return AudioSegment.from_file("audio/" + random.choice(haiku), format="wav")

def get_clip(action):
    audio_name = ""
    if action == "LEFT":
        return left_audio
    elif action == "MIDDLE":
        return middle_audio
    elif action == "RIGHT":
        return right_audio
    else:
        return wires_audio
                
def play_sound(action):
    play(get_clip(action))

def get_time():
    return time.time_ns() / 1000 / 1000

def button_left_pressed():
    global current_action
    global completed_action
    global left_button_pressed
    global lost
    
    if not left_button_pressed and completed_action == False:
        if current_action == "LEFT":
            completed_action = True
        else:
            lost = True
    left_button_pressed = True

def button_left_released():
    global left_button_pressed
    left_button_pressed = False

def button_middle_pressed():
    global current_action
    global completed_action
    global middle_button_pressed
    global lost
    
    if not middle_button_pressed and completed_action == False:
        if current_action == "MIDDLE":
            completed_action = True
        else:
            lost = True
    middle_button_pressed = True

def button_middle_released():
    global middle_button_pressed
    middle_button_pressed = False

def button_right_pressed():
    global current_action
    global completed_action
    global right_button_pressed
    global lost
    
    if not right_button_pressed and completed_action == False:
        if current_action == "RIGHT":
            completed_action = True
        else:
            lost = True
    right_button_pressed = True

def button_right_released():
    global right_button_pressed
    right_button_pressed = False

def button_wires_pressed():
    global current_action
    global completed_action
    global wires_button_pressed
    global lost
    
    if not wires_button_pressed and completed_action == False:
        if current_action == "WIRES":
            completed_action = True
        else:
            lost = True
    wires_button_pressed = True

def button_wires_released():
    global wires_button_pressed
    wires_button_pressed = False

left_button.when_pressed = button_left_pressed
left_button.when_released = button_left_released

middle_button.when_pressed = button_middle_pressed
middle_button.when_released = button_middle_released

right_button.when_pressed = button_right_pressed
right_button.when_released = button_right_released

wires_button.when_pressed = button_wires_pressed
wires_button.when_released = button_wires_released

green_led.on()

song = AudioSegment.from_file("audio/Intro.wav", format="wav")
#play(song)

green_led.off()
left_red_led.on()
right_red_led.on()

while not lost and not won:
    if completed_action:
        completed_actions += 1
        if completed_actions >= button_presses_to_win:
            won = True
            break
        elif completed_actions >= button_presses_to_win / 2:
            left_red_led.off()
        current_action = random.choice(actions)
        print(current_action)
        completed_action = False
        play_sound(current_action)
        step_time = step_time * 0.95
        step_start = get_time()
        print("STEP: " + str(step_start))
    elif get_time() > step_start + int(step_time):
        print("LOST")
        lost = True   


if lost:
    left_red_led.on()
    right_red_led.on()
    uv_led.on()
    song = AudioSegment.from_file("audio/Lose.wav", format="wav")
    play(song)
    
    sleep(2)
    
    song = get_lose_haiku()
    play(song)
elif won:
    left_red_led.off()
    right_red_led.off()
    sleep(1)
    green_led.on()
    song = AudioSegment.from_file("audio/Win.wav", format="wav")
    play(song)
    sleep(2)
    song = get_win_haiku()
    play(song)
    with open("wins.txt", "w") as file:
        file.write(str(current_win_count + 1))
   

print("GAME_COMPLETED")
