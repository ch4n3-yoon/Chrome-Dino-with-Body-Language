import os
from selenium import webdriver
import Web.server as Server


class App:
    def __init__(self):
        self.cam_browser = None
        self.game_browser = None

    def init_server(self):
        Server.init_server()

    def init_browser(self):
        chrome_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'chromedriver.exe')
        self.cam_browser = webdriver.Chrome(chrome_path)
        self.cam_browser.get('http://localhost:5000/cam')

        self.game_browser = webdriver.Chrome(chrome_path)
        self.game_browser.get('chrome://dino')

        print("[*] Initializing Chrome browser")

    def run(self):
        self.init_server()
        self.init_browser()

if __name__ == '__main__':
    app = App()
    app.run()
