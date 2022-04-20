##################################################################
#                       TO DO: 12-01-2020                        #
# -------------------------------------------------------------- #
#                                                                #
#   3. [MED. PRIORITY]  Fix Encryption                           #
#   4. [MED. PRIORITY]  Try to "break" program for debugging     #
#   5. [LOW PRIORITY]   Check results of return login
#   5. [LOW PRIORITY]   Clean up code & add comments             #
#   6. [LOWEST PRIORITY] Improve GUI aesthetics                  #
##################################################################
import base64
import sqlite3
import PySimpleGUI as sg
import pygamepong
import flappy_bird
import space_invaders
import snake
import datetime
import string
from os import environ
from os.path import dirname, abspath, join
from sqlite3 import Error
from cryptography.fernet import Fernet
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

# Encryption
key = Fernet.generate_key()
cipher_suite = Fernet(key)
conn = None
cursor = None
DEBUG = True


def get_top_players(table):
    cursor.execute("SELECT username, score, datetime FROM " + table + " GROUP BY username, score ORDER BY score DESC LIMIT 25;")
    row = cursor.fetchall()
    conn.commit()
    return row

def view_stats(self):
    # pull from db and print out in pop-up window
    fl_return_list = []
    sp_return_list = []
    po_return_list = []
    sn_return_list = []

    # query the database for the player's top 5 scores in Flappy Bird
    cursor.execute(
        "SELECT username, score AS f_score, STRFTIME('%d/%m/%Y', datetime) AS f_date FROM flappy WHERE username=? ORDER BY score DESC LIMIT 5;",
        (self.get_username(),))
    f_rows = cursor.fetchall()
    conn.commit()

    if f_rows:
        for element in f_rows:
            fl_return_list.append(element)
    else:
        fl_return_list.append((0, 0, 0))

    # query the database for the player's top 5 scores in Space Invaders
    cursor.execute(
        "SELECT username, score AS sp_score, STRFTIME('%d/%m/%Y', datetime) AS sp_date FROM space WHERE username=? ORDER BY score DESC LIMIT 5;",
        (self.get_username(),))
    sp_rows = cursor.fetchall()
    conn.commit()

    if sp_rows:
        for element in sp_rows:
            sp_return_list.append(element)
    else:
        sp_return_list.append((0, 0, 0))

    # query the database for the player's top 5 scores in Pong
    cursor.execute(
        "SELECT username, score AS p_score, STRFTIME('%d/%m/%Y', datetime) AS p_date FROM pong WHERE username=? ORDER BY score DESC LIMIT 5;",
        (self.get_username(),))
    p_rows = cursor.fetchall()
    conn.commit()

    if p_rows:
        for element in p_rows:
            po_return_list.append(element)
    else:
        po_return_list.append((0, 0, 0))

    # query the database for the player's top 5 scores in Snake
    cursor.execute(
        "SELECT username, score AS sn_score, STRFTIME('%d/%m/%Y', datetime) AS sn_date FROM snake WHERE username=? ORDER BY score DESC LIMIT 5;",
        (self.get_username(),))
    sn_rows = cursor.fetchall()
    conn.commit()

    if sn_rows:
        for element in sn_rows:
            sn_return_list.append(element)
    else:
        sn_return_list.append((0, 0, 0))

    # returns list with scores ordered: flappy bird, space invaders, pong, snake
    return fl_return_list, sp_return_list, po_return_list, sn_return_list

def view_leaderboard():
    # pull from db and print out in pop-up window
    lb_fl_return_list = []
    lb_sp_return_list = []
    lb_po_return_list = []
    lb_sn_return_list = []

    # query the database for the Top 5 scores in Flappy Bird
    
    lb_f_rows = get_top_players("flappy")
    
    if lb_f_rows:
        for f_element in lb_f_rows:
            lb_fl_return_list.append(f_element)
    else:
        lb_fl_return_list.append((0, 0, 0))

    # query the database for the Top 5 scores in Space Invaders
    lb_space_rows = get_top_players("space")
   
    if lb_space_rows != []:
        for sp_element in lb_space_rows:
            lb_sp_return_list.append(sp_element)
    else:
        lb_sp_return_list.append((0, 0, 0))

    # query the database for the Top 5 scores in Pong
    lb_po_rows = get_top_players("pong")
 
    if lb_po_rows != []:
        for po_element in lb_po_rows:
            lb_po_return_list.append(po_element)
    else:
        lb_po_return_list.append((0, 0, 0))
   
    # query the database for the Top 5 scores in Snake
    lb_sn_rows = get_top_players("pong")
   
    if lb_sn_rows:
        for sn_element in lb_sn_rows:
            lb_sn_return_list.append(sn_element)
    else:
        lb_sn_return_list.append((0, 0, 0))
    
    # returns list with scores ordered: flappy bird, space invaders, pong, snake
    return lb_fl_return_list, lb_sp_return_list, lb_po_return_list, lb_sn_return_list


def encrypt(pwd):
    print("[Encrypt] Plain Password: ", pwd)
    pwd_ascii = pwd.encode("ascii")  # set encoding to ascii
    pwd_bytes = base64.b64encode(pwd_ascii)  # convert password to bytes
    print("[Encrypt] Password in bytes: ", pwd_bytes)
    encrypted_password = cipher_suite.encrypt(pwd_bytes)  # Encrypt with AES
    print("[Encrypt] Encrypted Password: ", encrypted_password)
    return encrypted_password


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


# Player class
class Player:
    _User = None
    _Pass = None
    _is_logged_in = False

    # Default constructor
    def __init__(self):
        if not values and DEBUG:
            print("[Player] Values is None...")
        else:
            self._User = values.get('Username')
            self._Pass = values.get('Password')

    def __del__(self):
        self._is_logged_in = False
        self._User = None
        self._Pass = None
        if conn:
            conn.close()

    def get_username(self):
        if not self._User:
            if DEBUG:
                print("Error: Username is None!")
        return self._User

    def get_password(self):
        if not self._Pass and DEBUG:
            print("Error: Password is None!")
            self._Pass = "default_because_none_error"
        return self._Pass

    def get_login_status(self):
        return self._is_logged_in

    @staticmethod
    def invalid_username(desired_username):
        if any(not c.isalnum() for c in desired_username):
            if DEBUG:
                print("Username contains invalid characters. ONLY ALPHANUM ALLOWED!")
            return False
        return True

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

    def register(self, register_uname, pwd):
        _Username = register_uname
        _Pass = pwd
        # ##### SOME POP UP FOR THIS? ############
        if not self.invalid_username(register_uname):
            if DEBUG:
                print("Error: Username can only contain alphanumeric characters.")
            return 4
        else:
            cursor.execute("INSERT OR IGNORE INTO user(username, password) VALUES(?,?);",
                           (_Username, _Pass))
            conn.commit()  # finalize transaction
            if DEBUG:
                print("[SQLite] Success: Added username: ", player.get_username(), "\t with password: ",
                      player.get_password())
            return 0
    def login(self, login_uname, pwd):
        if self._is_logged_in:
            self._is_logged_in = False  # make sure class variable '_is_logged_in' is set to False before trying to login
        try:
            if not login_uname or not pwd:
                return 1
            else:
                cursor.execute(
                    "SELECT DISTINCT username, password FROM user WHERE user.username = ? AND user.password = ?",
                    (login_uname, pwd))
                login_rows = cursor.fetchall()
                conn.commit()
                num_rows = len(login_rows)

                # We found one and only one match
                if num_rows == 1:
                    if DEBUG:
                        print("[SQLite] Login Successful!")
                    self._is_logged_in = True
                    self.set_login_status(1)
                    return 0

                # We found no matches
                elif num_rows <= 0:
                    if DEBUG:
                        print("[SQLite] No records found...")
                    self._is_logged_in = False
                    return -1

                # We found duplicates --> this should not be possible.
                elif num_rows > 1:
                    if DEBUG:
                        print("[SQLite] Duplicate records found... # = ", num_rows)
                    return 2

                else:
                    if DEBUG:
                        print("[SQLite] Unknown failure fetching username & password.")
                    return 3
        except Error as e:
            if DEBUG:
                print("[SQLite] login query failed. Error: ", e)
            return 3

    def view_stats(self):
        # pull from db and print out in pop-up window
        fl_return_list = []
        sp_return_list = []
        po_return_list = []
        sn_return_list = []

        # query the database for the player's top 5 scores in Flappy Bird
        cursor.execute(
            "SELECT username, score AS f_score, STRFTIME('%d/%m/%Y', datetime) AS f_date FROM flappy WHERE username=? ORDER BY score DESC LIMIT 5",
            (self.get_username(),))
        f_rows = cursor.fetchall()
        conn.commit()

        if f_rows != []:
            for element in f_rows:
                fl_return_list.append(element)
        else:
            fl_return_list.append((0,0,0))

        # query the database for the player's top 5 scores in Space Invaders
        cursor.execute(
            "SELECT username, score AS sp_score, STRFTIME('%d/%m/%Y', datetime) AS sp_date FROM space WHERE username=? ORDER BY score DESC LIMIT 5",
            (self.get_username(),))
        sp_rows = cursor.fetchall()
        conn.commit()

        if sp_rows != []:
            for element in sp_rows:
                sp_return_list.append(element)
        else:
            sp_return_list.append((0, 0, 0))

        # query the database for the player's top 5 scores in Pong
        cursor.execute(
            "SELECT username, score AS p_score, STRFTIME('%d/%m/%Y', datetime) AS p_date FROM pong WHERE username=? ORDER BY score DESC LIMIT 5",
            (self.get_username(),))
        p_rows = cursor.fetchall()
        conn.commit()

        if p_rows != []:
            for element in p_rows:
                po_return_list.append(element)
        else:
            po_return_list.append((0, 0, 0))

        # query the database for the player's top 5 scores in Snake
        cursor.execute(
            "SELECT username, score AS sn_score, STRFTIME('%d/%m/%Y', datetime) AS sn_date FROM snake WHERE username=? ORDER BY score DESC LIMIT 5",
            (self.get_username(),))
        sn_rows = cursor.fetchall()
        conn.commit()

        if sn_rows != []:
            for element in sn_rows:
                sn_return_list.append(element)
        else:
            sn_return_list.append((0, 0, 0))

        # returns list with scores ordered: flappy bird, space invaders, pong, snake
        return fl_return_list, sp_return_list, po_return_list, sn_return_list


# Create the Main Window
main_window = sg.Window('RETRO ARCADE', main_layout, size=(852, 480))
player = Player()
count = 0
while True:
    if DEBUG:
        count = count + 1
        if count == 1 and DEBUG:
            print("[System] Inside \'while True\' loop. Execution count = ", count)
        elif count > 1 and DEBUG:
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
                player.set_username(values.get('Username'))
                player.set_password(values.get('Password'))
                login_status = player.login(player.get_username(), player.get_password())
                if login_status == -1:
                    unsuccessful_info = True
                elif login_status == 0:
                    successful_info = True

            except Error as error:
                if DEBUG:
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
                player.set_username(username)
                player.set_password(password)
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
            
    elif games_window_open:
        event, values = games_window.read()
        # DISPLAY GAMES

        if event == "Flappy Bird":
            print("[GAME] PLAY FLAPPY BIRD")
            
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
                                              VALUES (?, ?, ?)""",
                                                  (player.get_username(), score, datetime.datetime.now()))
                conn.commit()  # finalize and end transaction with database
                print("[SQLite] Flappy Bird HS added successfully.")

        elif event == "Pong":
           
            print("[GAME] PLAY PONG")
            # returns score
            pong_score = pygamepong.PongGame()

            if pong_score is None:
                print("[SQLite] Pong Insertion Error...Point value must be > 0.")
                break
            elif player.get_username() is None:
                print("[SQLite] Pong Insertion Error...Username is null. ")
                break
            else:
                sql_pong_query = cursor.execute("""INSERT INTO pong(username,score,datetime) VALUES (?,?,?)""",
                                                (player.get_username(), pong_score, datetime.datetime.now()))
                conn.commit()  # finalize transaction with database
                print("Pong HS added successfully.")

        elif event == "Space Invaders":
            print("[GAME] PLAY SPACE INVADERS")
            # RETURNS SCORE!!!
            score = space_invaders.SI_Game()
            print(score)
            if score is None:
                print("[SQLite] Space Invaders Insertion Error...Point value must be > 0.")
                break
            elif player.get_username() is None:
                print("[SQLite] Space Invaders Insertion Error...Username is null. ")
                break
            else:
                sql_space_query = cursor.execute("""INSERT INTO space(username,score,datetime) VALUES (?,?,?)""",
                                                 (player.get_username(), score, datetime.datetime.now()))
                conn.commit()  # finalize transaction with database
                print("Space Invaders HS added successfully.")

        elif event == "Snake":
            print("[GAME] PLAY SNAKE")
            # returns score!
            snake_score = snake.Snake()

            if snake_score is None:
                print("[SQLite] Snake Insertion Error...Point value must be > 0.")
                break
            elif player.get_username() is None:
                print("[SQLite] Snake Insertion Error...Username is null. ")
                break
            else:
                sql_pong_query = cursor.execute("""INSERT INTO snake(username,score,datetime) VALUES (?,?,?)""",
                                                (player.get_username(), snake_score, datetime.datetime.now()))
                conn.commit()  # finalize transaction with database
                print("Snake HS added successfully.")

        elif event == 'My Stats':
            if DEBUG:
                print("[USER] VIEW STATS")

            # stats_list = player.view_stats()
            # stats_string = player.get_username() + "'s High Scores\n*******************\nFlappy Bird:\t" + str(stats_list[0]) + ' ' + str(stats_list[1]) + (stats_list[2]) + "\nSpace Invaders:\t" + str(stats_list[1]
            #         ) + "\nPong:\t" + str(stats_list[2]
            #         )  + "\nSnake:\t" + str(stats_list[3])
            fl_stats_list, sp_stats_list, po_stats_list, sn_stats_list = player.view_stats()
            stats_string = player.get_username() + "'s High Scores\n*******************\n\tFlappy " \
                                                     "Bird:\n\t-------------------------"
            while len(fl_stats_list) != 5:
                fl_stats_list.append((0,0,0))
            counter = 1
            for score in fl_stats_list:
                stats_string += "\n\t " + str(counter) + ". " + str(score[1])
                counter += 1

            stats_string += "\n\n\tSpace Invaders:\n\t-------------------------"
            while len(sp_stats_list) != 5:
                sp_stats_list.append((0,0,0))
            counter = 1
            for score in sp_stats_list:
                stats_string += "\n\t " + str(counter) + ". " + str(score[1])
                counter += 1

            stats_string += "\n\n\tPong:\n\t-------------------------"
            while len(po_stats_list) != 5:
                po_stats_list.append((0,0,0))
            counter = 1
            for score in po_stats_list:
                stats_string += "\n\t " + str(counter) + ". " + str(score[1])
                counter += 1

            stats_string += "\n\n\tSnake:\n\t-------------------------"
            while len(sn_stats_list) != 5:
                sn_stats_list.append((0,0,0))
            counter = 1
            for score in sn_stats_list:
                stats_string += "\n\t " + str(counter) + ". " + str(score[1])
                counter += 1
                                                                
            sg.popup_scrolled(stats_string, title=player.get_username(), font=16)


        elif event == 'High Scores':

            if DEBUG:
                print("[USER] Overall High scores")

            high_score_string = ""

            # iterate through all data, or we could have a high scores

            high_score_string += "Overall High Scores\n---------------------\n\n"

            lb_fl_high_score_list, lb_sp_high_score_list, lb_po_high_score_list, lb_sn_high_score_list = view_leaderboard()

            high_score_string = "Leaderboards\n*******************\n\tFlappy " \
 \
                                "Bird:\n\t-------------------------"

            while len(lb_fl_high_score_list) != 25:
                lb_fl_high_score_list.append((0, 0, 0))

            counter = 1

            for score in lb_fl_high_score_list:
                high_score_string += "\n\t " + str(counter) + ". " + str(score[0]) + " " + str(score[1])

                counter += 1

            high_score_string += "\n\n\tSpace Invaders:\n\t-------------------------"

            while len(lb_sp_high_score_list) != 25:
                lb_sp_high_score_list.append((0, 0, 0))

            counter = 1

            for score in lb_sp_high_score_list:
                high_score_string += "\n\t " + str(counter) + ". " + str(score[0]) + " " + str(score[1])

                counter += 1

            high_score_string += "\n\n\tPong:\n\t-------------------------"

            while len(lb_po_high_score_list) != 25:
                lb_po_high_score_list.append((0, 0, 0))

            counter = 1

            for score in lb_po_high_score_list:
                high_score_string += "\n\t " + str(counter) + ". " + str(score[0]) + " " + str(score[1])

                counter += 1

            high_score_string += "\n\n\tSnake:\n\t-------------------------"

            while len(lb_sn_high_score_list) != 25:
                lb_sn_high_score_list.append((0, 0, 0))

            counter = 1

            for score in lb_sn_high_score_list:
                high_score_string += "\n\t " + str(counter) + ". " + str(score[0]) + " " + str(score[1])

                counter += 1
             # high score popup
            sg.popup_scrolled(high_score_string, title="Retro Arcade Leaderboard", font=16)


        elif event == 'Top Players':
            # top player string that will be printed out in popup
            punc = '''!()-[]{};:'"\ <>./?@#$%^&*_~'''
            top_string = "\t\tTop 10 Players\n-------------------------------------------------\n\nFlappy Bird:\n"

            # FLAPPY BIRD TOP 10

            cursor.execute("""SELECT username, score
                                           FROM flappy
                                           GROUP BY username, score
                                           ORDER BY score DESC
                                           LIMIT 10 OFFSET 1""")
            lb_frows = cursor.fetchall()
            conn.commit()

            num = 1
            for element in lb_frows:
                toString = str(element)
                uname, points = toString.split(',')
                for ele in uname:
                    if ele in punc:
                        uname = uname.replace(ele, "")
                top_string += "\t" + str(num) + ".\t" + uname + '\n'
                num += 1
            num = 0
            top_string += "\n"

            # SPACE INVADER TOP 10
            cursor.execute("""SELECT username, score
                                                       FROM space
                                                       GROUP BY username, score
                                                       ORDER BY score DESC
                                                       LIMIT 10 OFFSET 1""")
            lb_sp_rows = cursor.fetchall()
            conn.commit()
            top_string += "Space Invaders:\n"
            num = 1
            for element in lb_sp_rows:
                toString = str(element)
                uname, points = toString.split(',')
                for ele in uname:
                    if ele in punc:
                        uname = uname.replace(ele, "")
                top_string += "\t" + str(num) + ".\t" + uname + '\n'
                num += 1
            num = 0
            top_string += '\n'

            # PONG TOP 10
            cursor.execute("""SELECT username, score
                                                                   FROM pong
                                                                   GROUP BY username, score
                                                                   ORDER BY score DESC
                                                                   LIMIT 10 OFFSET 1""")
            lb_po_rows = cursor.fetchall()
            conn.commit()
            top_string += "Pong:\n"

            num = 1

            for element in lb_po_rows:
                toString = str(element)
                uname, points = toString.split(',')
                for ele in uname:
                    if ele in punc:
                        uname = uname.replace(ele, "")
                top_string += "\t" + str(num) + ".\t" + uname + '\n'
                num += 1
            num = 0


            # SNAKE TOP 5
            cursor.execute("""SELECT username, score
                                                                               FROM snake
                                                                               GROUP BY username, score
                                                                               ORDER BY score DESC
                                                                               LIMIT 10 OFFSET 1""")
            lb_sn_rows = cursor.fetchall()
            conn.commit()
            top_string += "\nSnake:\n"
            num = 1
            for element in lb_sn_rows:
                toString = str(element)
                uname, points = toString.split(',')
                for ele in uname:
                    if ele in punc:
                        uname = uname.replace(ele, "")
                top_string += "\t" + str(num) + ".\t" + uname + '\n'
                num += 1
            num = 0

            # prints out top players for all of the games
            sg.popup_scrolled(top_string, title="Top Players", font=16)

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
                sg.popup_ok('Please enter information into ALL fields.', title="Invalid Entry", font=14)
            elif unsuccessful_info:
                sg.popup_ok('Username already taken. Please enter another.', title="Invalid Entry", font=14)
            elif successful_info:

                Username = values.get('Username')
                Password = values.get('Password')
                if player.register(Username, Password) == 4:
                    sg.popup_ok('Invalid characters entered. Please enter another.', title="Invalid Entry", font=14)
                    successful_info = False
                    unsuccessful_info = True
                else:
                    player.set_login_status("True")
                    sql_signup_query = cursor.execute("INSERT OR IGNORE INTO user(username, password) VALUES(?,?);",
                                                  (player.get_username(), player.get_password(),))
                    conn.commit()  # finalize transaction
                    print("[SQLite] Success: Added username: ", player.get_username(), "\t with password: ",
                      player.get_password())

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
                player.login(player.get_username(), player.get_password())

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
                             sg.Button("Top Players", font=16, button_color=('dark grey', 'dark violet')),
                             sg.Button("Sign Out", font=16, button_color=('dark grey', 'dark violet')),
                             sg.Cancel("Exit", font=16, button_color=('dark grey', 'dark violet'))],
                            [sg.Button("Flappy Bird", font=16, button_color=('dark grey', 'dark violet')),
                             sg.Button("Pong", font=16, button_color=('dark grey', 'dark violet'))],
                            [sg.Button("Snake", font=16, button_color=('dark grey', 'dark violet')),
                             sg.Button("Space Invaders", font=16, button_color=('dark grey', 'dark violet'))],
                            [sg.Image("1.png")]]

            # creates/opens game display window
            games_window = sg.Window('RETRO ARCADE', games_layout, size=(852, 480))

            games_window_open = True
