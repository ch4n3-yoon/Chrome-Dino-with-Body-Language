
# For import keyboard.py
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

import keyboard
from flask import Flask, render_template
from flask_cors import CORS
import threading
import time


app = Flask(__name__)
CORS(app, resources={r'*': {'origins': '*'}})

@app.route('/jump')     
def jump():
    keyboard.send_spacebar()
    time.sleep(1)
    return ''


@app.route('/cam')
def cam():
    return render_template('tf_cam.html')


@app.route('/game')
def game():
    return render_template('chrome-dino.html')


def init_server():
    threading.Thread(target=app.run).start()


if __name__ == '__main__':
    app.run()