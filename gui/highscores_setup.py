# Retro Arcade CEN4090L Project
# filename: highscores_setup.py
# author: Andrew

import sqlite3
from sqlite3 import Error

database = "retro-arcade.db"

sql_create_game_table = """CREATE TABLE IF NOT EXISTS "game" (
                            
                                gid integer not null
                                    constraint game_pk
                                        primary key autoincrement,
                                title text "");
                                
                                    create unique index game_gid_uindex
                                        on game (gid);
                                    
                                    create unique index game_title_uindex
                                        on game (title);"""

sql_create_pong_table = """CREATE TABLE IF NOT EXISTS "pong" (
                            
                                id text(40) not null
                                primary key,
                                max integer(20),
                                time timestamp,
                                date datetime,
                                "limit" int);"""

sql_create_user_table = """CREATE TABLE IF NOT EXISTS "user" (
                                username text not null,
                                password text,
                                favorites text,
                                uid integer not null
                                constraint user_pk
                                primary key autoincrement);
                                
                                create unique index user_uid_uindex
                                    on user (uid);
                                    
                                create unique index user_username_uindex
                                        on user (username); """


sql_create_user_pong_history_table = """CREATE TABLE IF NOT EXISTS "user_top5_pong" (
                                uid int unique primary key, 
                                hs_1 int,
                                hs_2 int,
                                hs_3 int,
                                hs_4 int,
                                hs_5 int,
                                hs_1_time datetime,
                                hs_2_time datetime,
                                hs_3_time datetime,
                                hs_4_time datetime,
                                hs_5_time datetime);"""


def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):  # create table
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def setup():
    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        create_table(conn, sql_create_game_table)  # create game table
        create_table(conn, sql_create_pong_table)  # create pong table
        create_table(conn, sql_create_user_table)  # create user table
        create_table(conn, sql_create_user_pong_history_table)  # create user_history table

    else:
        print("Error! cannot create the database connection.")


if __name__ == '__highscores_setup__':
    setup()
