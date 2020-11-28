import base64
import sqlite3
from cryptography.fernet import Fernet
from os import environ
from os.path import dirname, abspath, join
from sqlite3 import Error

environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import PySimpleGUI as sg
import pygamepong
import flappy_bird
import space_invaders
import snake
import datetime as datetime
import time as time


# Encryption
key = Fernet.generate_key()
cipher_suite = Fernet(key)
conn = None
cursor = None





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



event = None  # Event Loop to process "events"
values = None
signin_window = None
signup_window = None
games_window = None

ROOT_DIR = dirname(dirname(abspath(__file__)))

sg.theme('Dark Purple 4')
sg.SetOptions(input_text_color='white')

main_layout = [[sg.Button("Sign Up", font=16, button_color=('dark grey', 'dark violet')),
                sg.Button("Sign In", font=16, button_color=('dark grey', 'dark violet')),
                sg.Button("Exit", font=16, button_color=('dark grey', 'dark violet'))],
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


class Player:
    _User = "None"
    _Pass = ""
    _is_logged_in = False

    def get_username(self):
        return self._User

    def get_password(self):
        return self._Pass

    def get_login_status(self):
        return self._is_logged_in

    def set_username(self, set_string):
        self._User = set_string

    def set_password(self, set_string):
        self._Pass = set_string

    def set_login_status(self, set_bool):
        if self._is_logged_in and set_bool == "False" or set_bool == 0:
            self._is_logged_in = False
        elif not self._is_logged_in and set_bool == "True" or set_bool == 1:
            self._is_logged_in = True
        else:
            self._is_logged_in = False

def encrypt(pwd):
    print("Plain Password: ", pwd)
    pwd_ascii = pwd.encode("ascii")  # set encoding to ascii
    pwd_bytes = base64.b64encode(pwd_ascii)  # convert password to bytes
    encrypted_password = cipher_suite.encrypt(pwd_bytes)  # Encrypt with AES
    print("Encrypted Password: ", encrypted_password)
    return encrypted_password
# Create the Main Window
main_window = sg.Window('RETRO ARCADE', main_layout, size=(852, 480))
player = Player()
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
                User = values.get('Username')
                Pass = encrypt(values.get('Password'))

                print(player.get_password())

                sql_login_query = cursor.execute("SELECT DISTINCT username,password "
                                                 "FROM user WHERE user.username = ? "
                                                 "AND user.password = ?", (player.get_username(), player.get_password()))
                rows = cursor.fetchall()
                conn.commit()  # finalize and end transaction with database
                num_rows = len(rows)

                if num_rows < 0:
                    print("[SQLite] Username/Password combination not found in the database.")
                    events, value = signin_window.read()
                    break
                elif num_rows == 1:
                    print("[SQLite] Login successful.")  # -> if valid, open games_window
                    player.set_login_status("True")
                    successful_info = True
                elif num_rows > 1:
                    print("[SQLite] Duplicate record(s) found.")
                    break
                else:
                    print("[SQLite] Unknown failure fetching username & password.")
                    unsuccessful_info = True
                    #break
            except Error as error:
                print("[SQLite] login query failed to fetch record. Error: ", error)
                player.set_login_status("False")
                break

    elif signup_window_open:
        if final_sign_up:
            event = 'Sign Up'
            signup_window.close()
            final_sign_up = False
        elif unsuccessful_info:
            event = 'Sign Up'
            signup_window.close()
            unsuccessful_info = False
        else:
            event, values = signup_window.read()
            try:
                username = values.get('Username')
                password = values.get('Password')
                player.set_username(values.get('Username'))
                player.Pass = password
                sql_check_available = cursor.execute(
                    "SELECT username COLLATE NOCASE FROM user")  # Retrieve username to lowercase
                rows = cursor.fetchall()

                for element in rows:
                    if username == element[0]:
                        print("[SQLite] Username found in database. Please try another.")
                        unsuccessful_info = True
                        break

                if not unsuccessful_info:
                    print("[SQLite] Username is available!")
                    successful_info = True
                    
            except Error as error:
                print("[SQLite] Signup query failed to fetch record. Error: ", error)
                break
               
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
            elif player.get_username() is None:
                print("[SQLite] Flappy Bird Insertion Error...Username is null. ")
                break
            else:
                sql_flappy_query = cursor.execute("""INSERT INTO flappy(username,score,datetime)
                                              VALUES (?, ?, ?)""", (player.get_username(), score, datetime.datetime.now()))
                conn.commit()  # finalize and end transaction with database
                print("[SQLite] Flappy Bird HS added successfully.")

        elif event == "Pong":
            print("[GAME] PLAY PONG")
            #returns score
            pong_score = pygamepong.PongGame()

            if pong_score is None:
                print("[SQLite] Flappy Bird Insertion Error...Point value must be > 0.")
                break
            elif player.get_username() is None:
                print("[SQLite] Flappy Bird Insertion Error...Username is null. ")
                break
            else:
                sql_pong_query = cursor.execute("""INSERT INTO pong(username,score,datetime) VALUES (?,?,?)""", (player.get_username(), pong_score, datetime.datetime.now()))
                conn.commit() # finalize transaction with database
                print("Pong HS added successfully.")

        elif event == "Space Invaders":
            print("[GAME] PLAY SPACE INVADERS")
            # RETURNS SCORE!!!
            score = space_invaders.SI_Game()
            print(score)

        elif event == "Snake":
            print("[GAME] PLAY SNAKE")
            #returns score!
            snake_score = snake.Snake()

        elif event == 'My Stats':
            print("[USER] VIEW STATS")
            # pull from db and print out in pop-up window
            sql_stats_query = cursor.execute("SELECT * FROM flappy WHERE username = ?", (player.get_username(),))
            output = cursor.fetchall()
            conn.commit()
            flappy_high_score = 0
            for data in output:
                if data[0] == player.get_username():
                    if data[1] >= flappy_high_score:
                        flappy_high_score = data[1]
                        flappy_score_date = data[2]
            if flappy_high_score == 0:
                flappy_score_date = None

            #create a string with all of the player's personal stats for each game
            example_string = player.get_username() + "'s High Scores\nFlappy Bird: " + str(flappy_high_score) + "\nSpace Invaders: 3\nPong: 3\nSnake: 17"
            sg.popup(example_string, title = player.get_username() + " personal stats", font=14)
            #print out personal high scores, number of times played

        elif event == 'High Scores':
            print("[USER] High scores")
            sql_stats_query = cursor.execute("SELECT * FROM flappy")
            output = cursor.fetchall()
            conn.commit()
            #iterate through all data, or we could have a high scores
            flappy_high_score = 0
            for data in output:
                if data[0] != '':
                    if data[1] >= flappy_high_score:
                        flappy_high_score = data[1]
            if flappy_high_score == 0:
                flappy_score_date = None
            example_string = "High Scores\nFlappy Bird: " + str(flappy_high_score) + " (Username: " + data[0] + ")\nSpace Invaders: 3\nPong: 3\nSnake: 17"
            sg.popup(example_string, title="Retro Arcade High Scores", font=14)
        
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

            player.set_login_status("False")

    if event == 'Sign In':

        signin_layout = [[sg.Text("Username", font=16), sg.InputText('', key='Username', font=16)],
                         [sg.Text('Password  ', font=16), sg.InputText('', key='Password', password_char='*', font=16)],
                         [sg.OK("Finish Sign In", button_color=('dark grey', 'dark violet'), font=16),
                          sg.OK("Back", button_color=('dark grey', 'dark violet'), font=16),
                          sg.Cancel("Exit", font=16, button_color=('dark grey', 'dark violet'))], [sg.Image("./1.png")]]

        # creates/opens sign in window
        signin_window = sg.Window('RETRO ARCADE', signin_layout, size=(852, 480))

        signin_window_open = True
        main_window.hide()
        main_window_hidden = True

    elif event == 'Sign Up':
        print("sign up here")

        signup_layout = [[sg.Text("Username", font=16), sg.InputText('', key='Username', font=16)],
                         [sg.Text('Password  ', font=16), sg.InputText('', key='Password', password_char='*', font=16)],
                         [sg.OK("Complete Sign Up", font=16, button_color=('dark grey', 'dark violet')),
                          sg.OK("Back", font=16, button_color=('dark grey', 'dark violet')),
                          sg.Cancel("Exit", font=16, button_color=('dark grey', 'dark violet'))], [sg.Image("1.png")]]

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
                sg.popup_ok('Please enter information into ALL fields.', title = "Invalid Entry", font=14)
            elif unsuccessful_info:
                sg.popup_ok('Username already taken. Please enter another.', title = "Invalid Entry", font=14)
            elif successful_info:
                player.set_username(values.get('Username'))
                player._Pass = encrypt(values.get('Password'))

                player.set_login_status("True")
                sql_signup_query = cursor.execute("INSERT OR IGNORE INTO user(username, password) VALUES(?,?);",
                                                  (player.get_username(), player.get_password(),))
                conn.commit()  # finalize transaction
                print("[SQLite] Success: Added username: ", player.get_username(), "\t with password: ", player.get_password())

        # CHECK FOR COMPLETE FIELDS FOR SIGN IN
        else:
            # loop to check if info was entered into every field
            for value in values:
                if values[value] == '' or values[value] == '':
                    final_sign_in = True

            # pop up if user does not enter info into every field
            if final_sign_in:
                sg.popup_ok('Please enter both your username and password.', font=14)

            # pop up if user enters invalid info
            elif unsuccessful_info:
                sg.popup_ok('Information entered invalid. Please try again.', font=14)

            else:
                sql_login_query = cursor.execute("SELECT DISTINCT username,password "
                                                 "FROM user WHERE user.username = ? "
                                                 "AND user.password = ?", (player.get_username(), player.get_password()))

        # if all fields have been filled in -> still have to check if info provided is valid
        # could have another bool that we set to true only when user info has been confirmed
        if player.get_login_status():

            if signin_window_open:
                signin_window.close()
                signin_window_open = False
            else:
                signup_window.close()
                signup_window_open = False

            games_layout = [[sg.Text("Welcome to Retro Arcade " + player.get_username(), font=20)],
                            [sg.Button("My Stats", font=16, button_color=('dark grey', 'dark violet')),
                             sg.Button("High Scores", font=16, button_color=('dark grey', 'dark violet')),
                             sg.Button("Sign Out", font=16, button_color=('dark grey', 'dark violet')),
                             sg.Cancel("Exit", font=16, button_color=('dark grey', 'dark violet'))],
                            [sg.Button("Flappy Bird", font=16,button_color=('dark grey', 'dark violet')),
                             sg.Button("Pong", font=16, button_color=('dark grey', 'dark violet'))],
                            [sg.Button("Snake", font=16, button_color=('dark grey', 'dark violet')),
                             sg.Button("Space Invaders", font=16, button_color=('dark grey', 'dark violet'))],
                            [sg.Image("1.png")]]

            # creates/opens game display window
            games_window = sg.Window('RETRO ARCADE', games_layout, size=(852, 480))

            games_window_open = True
