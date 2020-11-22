import sqlite3
from os import environ
from os.path import dirname, abspath, join
from sqlite3 import Error

environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import PySimpleGUI as sg
import pong
import flappy_bird
import space_invaders
import snake
import datetime as datetime
import time as time

# Keep libraries in game code (don't need to add it here)
# comment out sys.exit() in game code (if present), add return value
# LAST STEP: MAKE IT ACTUALLY LOOK NICE
# booleans to display correct window
main_window_hidden = False
signup_window_hidden = False
signin_window_open = False
signup_window_open = False
games_window_open = False
final_sign_in = False
final_sign_up = False
successful_info = False
unsuccessful_info = False

user_logged_in = False
# User Login # login_success = False
# User Sign up # signup_success = False

User = None
Pass = None
conn = None
cursor = None
event = None  # Event Loop to process "events"
values = None
signin_window = None
signup_window = None
games_window = None

ROOT_DIR = dirname(dirname(abspath(__file__)))

sg.theme('Dark Purple 4')
sg.SetOptions(input_text_color='white')

main_layout = [[sg.Button("Sign Up", button_color=('dark grey', 'dark violet')),
                sg.Button("Sign In", button_color=('dark grey', 'dark violet')),
                sg.Button("Exit", button_color=('dark grey', 'dark violet'))],
               [sg.Image('1.png')]]

print("[System] Please wait: Retro-Arcade is initializing...")
print("[System] PROJECT ROOT DIR: ", ROOT_DIR)

# connect to db
try:
    conn = sqlite3.connect(join(ROOT_DIR, 'highscores/retro-arcade.db'))
    cursor = conn.cursor()
    print("[SQLite] Successfully connected to the database.")

except Error as error:
    print("[SQLite] Failed to connect to the database. Error: ", error)

# Create the Main Window
main_window = sg.Window('RETRO ARCADE', main_layout, size=(852, 480))

count = 0
while True:
    count = count + 1
    if count == 1:
        print("[System] Inside \'while True\' loop. Execution count = ", count)
    # elif count%10 == 0:
    else:
        print("[System] Returned to \'while True\' loop. Execution count = ", count)

    if not main_window_hidden:
        event, values = main_window.read()
    elif signin_window_open:

        # if info not entered in every field -> reload sign in window
        if final_sign_in:
            event = 'Sign In'
            signin_window.close()
            final_sign_in = False

        # if info entered is not found in database -> reload sign in window
        elif unsuccessful_info:
            event = 'Sign In'
            signin_window.close()
            unsuccessful_info = False

        # read sign in window
        else:
            event, values = signin_window.read()

            try:
                Username = values.get('Username')
                Pass = values.get('Password')

                # Attempt to hash password
                # Pass =
                # print(hashlib.sha256(Username+Pass))

                sql_login_query = cursor.execute("SELECT DISTINCT username,password "
                                                 "FROM user WHERE user.username = ? "
                                                 "AND user.password = ?", (Username, Pass))
                rows = cursor.fetchall()
                conn.commit()  # finalize and end transaction with database
                num_rows = len(rows)

                if num_rows < 0:
                    print("[SQLite] Username/Password combination not found in the database.")
                    events, value = signin_window.read()
                    break
                elif num_rows == 1:
                    print("[SQLite] Login successful.")  # -> if valid, open games_window
                    User = values.get("Username")
                    successful_info = True
                elif num_rows > 1:
                    print("[SQLite] Duplicate record(s) found.")
                    break
                else:
                    print("[SQLite] Unknown failure fetching username & password.")
                    unsuccessful_info = True
                    break
            except Error as error:
                print("[SQLite] login query failed to fetch record. Error: ", error)
                break
                # unsuccessful_info = True

            # here connect to db -> steps:
            # prereq: ALL INFO FIELDS MUST HAVE TEXT
            # 1. SELECT email, password FROM <user_info> WHERE email='<user_entry>' AND password='user_entry>';
            # -> if valid, open games_window
            # -> if invalid, popup with "INCORRECT INFO" Message, repeat 1

    elif signup_window_open:
        if final_sign_up:
            event = 'Sign Up'
            signup_window.close()
            final_sign_up = False
        else:
            event, values = signup_window.read()
            try:
                User = values.get('Username')
                Pass = values.get('Password')

                # Attempt to hash password
                # Pass = hashlib.sha256(Username+Pass)

                sql_check_available = cursor.execute(
                    "SELECT username COLLATE NOCASE FROM user")  # Retrieve username to lowercase
                rows = cursor.fetchall()

                for element in rows:
                    if User == element:
                        print("[SQLite] Username found in database. Please try another.")
                        break

                print("[SQLite] Username is available!")
                successful_info = True
                conn.commit()  # finalize and end transaction with database
                print("[SQLite] Signup succeeded")
            except Error as error:
                print("[SQLite] Signup query failed to fetch record. Error: ", error)
                break
                # unsuccessful_info = True

            # here is where we will access the db -> steps:
            # prereq: ALL INFO FIELDS MUST HAVE TEXT
            # 1. SELECT email FROM <user_info> WHERE email='<user_entry>';
            # -> if email not found, proceed to account creation and sign in -> games_window opens
            # ACCOUNT CREATION: INSERT INTO <user_info> VALUES (email, username, password);
            # -> if email found, popup with "ALREADY HAVE ACCOUNT WITH THIS EMAIL" message

    # NOTE: WHEN EXITING GAME, ENTIRE PROGRAM CLOSES -> FIX THIS
    elif games_window_open:
        event, values = games_window.read()
        # DISPLAY GAMES

        if event == "Flappy Bird":
            print("[GAME] PLAY FLAPPY BIRD")
            # RETURNS SCORE!!!
            score = flappy_bird.Flappy_Game()

            print("[GAME] Thanks for playing Flappy Bird! Score: ", score)

            if score is None:
                print("[SQLite] Flappy Bird Insertion Error...Point value must be > 0.")
                break
            elif User is None:
                print("[SQLite] Flappy Bird Insertion Error...Username is null. ")
                break
            else:
                sql_flappy_query = cursor.execute("""INSERT INTO flappy(username,score,datetime)
                                              VALUES (?, ?, ?)""", (User, score, datetime.datetime.now()))
                conn.commit()  # finalize and end transaction with database
                print("[SQLite] Flappy Bird HS added successfully.")

        elif event == "Pong":
            print("[GAME] PLAY PONG")
            pong.PongGame()

        elif event == "Space Invaders":
            print("[GAME] PLAY SPACE INVADERS")
            # RETURNS SCORE!!!
            score = space_invaders.SI_Game()
            print(score)

        elif event == "Snake":
            print("[GAME] PLAY SNAKE")
            snake.Snake()

        elif event == 'My Stats':
            print("[USER] VIEW STATS")
            # pull from db and print out in pop-up window
            sg.popup("My Stats")

        elif event == 'High Scores':
            print("[USER] High scores")
            sg.popup("High Scores")
            # pull from db and print out in pop-up window

        elif event == 'Sign Out':
            # returns to main window
            main_window.UnHide()
            main_window_hidden = False

            # closes game window
            games_window_open = False
            games_window.close()

            # sets login success to false until user signs in again
            unsuccessful_info = False
            successful_info = False
    # print(event, values)

    if event == 'Sign In':

        signin_layout = [[sg.Text("Username"), sg.InputText('', key='Username')],
                         [sg.Text('Password\t'), sg.InputText('', key='Password', password_char='*')],
                         [sg.OK("Finish Sign In", button_color=('dark grey', 'dark violet')),
                          sg.OK("Back", button_color=('dark grey', 'dark violet')),
                          sg.Cancel("Exit", button_color=('dark grey', 'dark violet'))], [sg.Image("./1.png")]]

        # creates/opens sign in window
        signin_window = sg.Window('RETRO ARCADE', signin_layout, size=(852, 480))

        signin_window_open = True
        main_window.hide()
        main_window_hidden = True

    elif event == 'Sign Up':
        print("sign up here")

        signup_layout = [[sg.Text("Username"), sg.InputText('', key='Username')],
                         [sg.Text('Password\t'), sg.InputText('', key='Password', password_char='*')],
                         [sg.OK("Complete Sign Up", button_color=('dark grey', 'dark violet')),
                          sg.OK("Back", button_color=('dark grey', 'dark violet')),
                          sg.Cancel("Exit", button_color=('dark grey', 'dark violet'))], [sg.Image("1.png")]]

        # creates/opens sign up window
        signup_window = sg.Window('RETRO ARCADE', signup_layout, size=(852, 480))

        signup_window_open = True
        main_window.hide()
        main_window_hidden = True

    elif event == 'Back':
        # returns to main window
        main_window.UnHide()
        main_window_hidden = False

        # closes previous window (either sign up or sign in windows)
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
        # CHECK FOR COMPLETE FIELDS FOR SIGN UP
        if signup_window_open:
            for value in values:
                if values[value] == '':
                    final_sign_up = True
            if final_sign_up:
                sg.popup_ok('Please enter information into ALL fields.')
            elif unsuccessful_info:
                sg.popup_ok('INFO INVALID. Please enter again.')
            elif successful_info:
                sql_signup_query = cursor.execute("INSERT OR IGNORE INTO user(username, password) VALUES(?,?);",
                                                  (User, Pass,))
                print("[SQLite] Success: Added username: ", User, "\t with password: ", Pass)
                conn.commit()  # finalize transaction
        # CHECK FOR COMPLETE FIELDS FOR SIGN IN
        else:
            # loop to check if info was entered into every field
            for value in values:
                if values[value] == '' or values[value] == '':
                    final_sign_in = True

            # pop up if user does not enter info into every field
            if final_sign_in:
                sg.popup_ok('Please enter both your username and password.')

            # pop up if user enters invalid info
            elif unsuccessful_info:
                sg.popup_ok('Information entered invalid. Please try again.')

        # if all fields have been filled in -> still have to check if info provided is valid
        # could have another bool that we set to true only when user info has been confirmed
        if (final_sign_up != True) and (final_sign_in != True) and (successful_info == True):

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

            # creates/opens game display window
            games_window = sg.Window('RETRO ARCADE', games_layout, size=(852, 480))

            games_window_open = True
