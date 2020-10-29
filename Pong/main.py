from flask import Flask, render_template, request
import pong
import datetime
import os
import sqlite3


app = Flask(__name__)


@app.route("/")  # (a) function to render the homepage for the root directory
# of the application
def main():
    return render_template("index.html")


@app.route('/pong')
def run_pong():
    return pong.Game()


if __name__ == '__main__':
    app.run()
