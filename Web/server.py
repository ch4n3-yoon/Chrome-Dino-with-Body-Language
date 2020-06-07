
# For import keyboard.py
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

import keyboard
from flask import Flask, render_template
from flask_cors import CORS
from flask_apscheduler import APScheduler
import threading
import time
import http


app = Flask(__name__)
CORS(app, resources={r'*': {'origins': '*'}})
func = keyboard.send_spacebar


@app.route('/cam')
def cam():
    return render_template('tf_cam.html')


@app.route('/game')
def game():
    return render_template('chrome-dino.html')


@app.route('/jump')
def jump():
    func()
    return '', http.HTTPStatus.NO_CONTENT


def init_server(jump_function=keyboard.send_spacebar):
    func = jump_function
    threading.Thread(target=app.run).start()


if __name__ == '__main__':
    app.run(debug=True, threaded=True, port=3000)
