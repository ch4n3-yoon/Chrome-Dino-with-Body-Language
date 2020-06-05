
# For import keyboard.py
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

import keyboard
from flask import Flask, render_template
import threading


app = Flask(__name__)


@app.route('/jump')
def jump():
    keyboard.send_spacebar()
    return ''


@app.route('/cam')
def cam():
    return render_template('tf_cam.html')


def init_server():
    # thread.start_new_thread(flaskThread, ())
    threading.Thread(target=app.run).start()
