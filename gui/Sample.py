import PySimpleGUI as sg
import sqlite3
from sqlite3 import Error
import importlib
import flappy_bird
import space_invaders
import pong
import snake
#import snake

#Keep libraries in game code (don't need to add it here)
#comment out sys.exit() in game code (if present), add return value
#LAST STEP: MAKE IT ACTUALLY LOOK NICE

sg.theme('Dark Purple 4')
sg.SetOptions(input_text_color='white')  

main_layout = [ [sg.Button("Sign Up", button_color=('dark grey', 'dark violet')), 
sg.Button("Sign In", button_color=('dark grey', 'dark violet')), 
sg.Button("Exit", button_color=('dark grey', 'dark violet'))], 
[sg.Image("1.png")]]

#connect to db
conn = sqlite3.connect('retro-arcade.db')

#Create the Main Window
main_window = sg.Window('RETRO ARCADE', main_layout, size=(852,480))

#booleans to display correct window 
main_window_hidden = False
signup_window_hidden = False
signin_window_open = False
signup_window_open = False
games_window_open = False
final_sign_in = False
final_sign_up = False

#Event Loop to process "events"
while True: 
    
    print("running")
     
    if not main_window_hidden:       
        event, values = main_window.read()
    elif signin_window_open:
        if final_sign_in:
            event = 'Sign In'
            signin_window.close()
            final_sign_in = False
        else:
            event, values = signin_window.read()

            #here connect to db -> steps:
            #prereq: ALL INFO FIELDS MUST HAVE TEXT
            #1. SELECT email, password FROM <user_info> WHERE email='<user_entry>' AND password='user_entry>';
            # -> if valid, open games_window
            # -> if invalid, popup with "INCORRECT INFO" Message, repeat 1
    elif signup_window_open:
        if final_sign_up:
            event = 'Sign Up'
            signup_window.close()
            final_sign_up = False
        else:
            event, values = signup_window.read()

            #here is where we will access the db -> steps:
            #prereq: ALL INFO FIELDS MUST HAVE TEXT
            #1. SELECT email FROM <user_info> WHERE email='<user_entry>';
            #-> if email not found, proceed to account creation and sign in -> games_window opens
                #ACCOUNT CREATION: INSERT INTO <user_info> VALUES (email, username, password);
            #-> if email found, popup with "ALREADY HAVE ACCOUNT WITH THIS EMAIL" message

    #NOTE: WHEN EXITING GAME, ENTIRE PROGRAM CLOSES -> FIX THIS
    elif games_window_open:
        event, values = games_window.read()
        #DISPLAY GAMES

        if event == "Flappy Bird":
            print("PLAY FLAPPY BIRD")
            #RETURNS SCORE!!!
            score = flappy_bird.Flappy_Game()
            print(score)

        elif event == "Pong":
            print("PLAY PONG")
            pong.PongGame()  

        elif event == "Space Invaders":
            print("PLAY SPACE INVADERS")
            #RETURNS SCORE!!!
            score = space_invaders.SI_Game()
            print(score)

        elif event == "Snake":
            print("PLAY SNAKE")
            snake.Snake()

        elif event == 'My Stats':
            print("VIEW STATS")
            #pull from db and print out in pop-up window
            sg.popup("My Stats")

        elif event == 'High Scores':
            print("High scores")
            sg.popup("High Scores")
            #pull from db and print out in pop-up window

        elif event == 'Sign Out':
            #returns to main window
            main_window.UnHide()
            main_window_hidden = False

            #closes game window
            games_window_open = False
            games_window.close()

    #print(event, values)
    
    if event == 'Sign In':
       
        signin_layout = [[sg.Text("Email\t"), sg.InputText('', key='Email')],
            [sg.Text('Password\t'), sg.InputText('', key='Password', password_char='*')],
            [sg.OK("Finish Sign In", button_color=('dark grey', 'dark violet')), 
            sg.OK("Back", button_color=('dark grey', 'dark violet')),
            sg.Cancel("Exit", button_color=('dark grey', 'dark violet'))], [sg.Image("1.png")]]
        
        #creates/opens sign in window
        signin_window = sg.Window('RETRO ARCADE', signin_layout, size=(852,480))

        signin_window_open = True
        main_window.hide()
        main_window_hidden = True
        
    elif event == 'Sign Up':
        print("sign up here")

        signup_layout = [[sg.Text("Email\t"), sg.InputText('', key='Email')],
                    [sg.Text("Username"), sg.InputText('', key='Username')], 
                    [sg.Text('Password\t'), sg.InputText('', key='Password', password_char='*')], 
                    [sg.OK("Complete Sign Up", button_color=('dark grey', 'dark violet')), 
                    sg.OK("Back", button_color=('dark grey', 'dark violet')),
                    sg.Cancel("Exit", button_color=('dark grey', 'dark violet'))], [sg.Image("1.png")]]

        #creates/opens sign up window
        signup_window = sg.Window('RETRO ARCADE', signup_layout, size=(852,480))

        signup_window_open = True
        main_window.hide()
        main_window_hidden = True
        

    elif event == 'Back':
        #returns to main window
        main_window.UnHide()
        main_window_hidden = False

        #closes previous window (either sign up or sign in windows)
        if signup_window_open:
            signup_window.close()
            signup_window_open = False
        else:
            signin_window.close()
            signin_window_open = False

    elif event in (sg.WIN_CLOSED, 'Exit'):
        main_window.close()
        break

    elif event == 'Complete Sign Up' or event == 'Finish Sign In':
        #CHECK FOR COMPLETE FIELDS FOR SIGN UP
        if signup_window_open:
            for value in values:
                if values[value] == '':
                    final_sign_up = True
            if final_sign_up:
                sg.popup_ok('Please enter information into ALL fields.')
        #CHECK FOR COMPLETE FIELDS FOR SIGN IN
        else:
            for value in values:
                if values[value] == '' or values[value] == '':
                    final_sign_in = True
            if final_sign_in:
                sg.popup_ok('Please enter both your email and password.')

        #if all fields have been filled in -> still have to check if info provided is valid
        #could have another bool that we set to true only when user info has been confirmed
        if (final_sign_up != True) and (final_sign_in != True):
            
            if signin_window_open:
                signin_window.close()
                signin_window_open = False
            else:
                signup_window.close()
                signup_window_open = False

            games_layout = [[sg.Button("My Stats", button_color=('dark grey', 'dark violet')), 
                    sg.Button("High Scores", button_color=('dark grey', 'dark violet')), 
                    sg.Button("Sign Out", button_color=('dark grey', 'dark violet')),
                    sg.Cancel("Exit", button_color=('dark grey', 'dark violet'))], 
                    [sg.Button("Flappy Bird", button_color=('dark grey', 'dark violet')), 
                    sg.Button("Pong", button_color=('dark grey', 'dark violet'))], 
                    [sg.Button("Snake", button_color=('dark grey', 'dark violet')), 
                    sg.Button("Space Invaders", button_color=('dark grey', 'dark violet'))], 
                    [sg.Image("1.png")]]

            #creates/opens game display window
            games_window = sg.Window('RETRO ARCADE', games_layout, size=(852,480))
                    
            games_window_open = True