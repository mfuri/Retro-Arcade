import PySimpleGUI as sg
# import trinket as tk
from pong import *
from flappy_bird import *
from space_invaders import *

sg.theme('Dark')

# STEP 1 Define the layout
layout = [
            [sg.Text('WELCOME TO THE RETRO ARCADE')],
            [sg.Text('What game would you like to play?')],
            [sg.Button('Pong'), sg.Button('Flappy Bird')],
            [sg.Button('Snake'), sg.Button('Space Invaders')]
         ]

# STEP 2 create the window
window = sg.Window('Retro Arcade', layout, grab_anywhere=True)

# STEP 3 - the event loop
while True:
    event, values = window.read()  # read event that happened
    print(event, values)
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    if event == 'Pong':
        Game()
        print('We need to run Pong')
    if event == 'Flappy Bird':
        Flappy_Game()
        print('We need to run Flappy Bird')
    if event == 'Snake':
        print('We need to run Snake')
    if event == 'Space Invaders':
        
        print('We need to run Space Invaders')
window.close()
