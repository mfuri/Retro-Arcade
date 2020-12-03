from flask import Flask, render_template, request
import Pong
import datetime
import os
import sqlite3

app = Flask(__name__)


@app.route("/")  # (a) function to render the homepage for the root directory
# of the application
def main():
    return render_template("index.html")


@app.route('/pong_leaderboard')
def pong_hs():
    con = sqlite3.connect("old_highscore/retro-arcade.db")
    con.row_factory = sqlite3.Row

    cur = con.cursor()
    cur.execute("SELECT * FROM pong ORDER BY score DESC LIMIT 10")

    rows = cur.fetchall()
    con.close()

    return render_template("pong_leaderboard.html", rows=rows)

@app.route('/playpong')
def run_pong():
    return run_pong.Game()


if __name__ == '__main__':
    app.run(ssl_context='adhoc')
