import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import Web.server as Server


def jump():
    app.game_browser.execute_script('tRexJump()')


class App:
    def __init__(self):
        self.cam_browser = None
        self.game_browser = None

    def init_server(self):
        Server.init_server(jump)

    def init_browser(self):

        # Add chrome selenium options to disable info box
        opt = Options()
        opt.add_argument("--disable-infobars")
        opt.add_argument("--disable-extensions")
        # Pass the argument 1 to allow and 2 to block
        opt.add_experimental_option("prefs", {
            "profile.default_content_setting_values.media_stream_mic": 1,
            "profile.default_content_setting_values.media_stream_camera": 1,
            "profile.default_content_setting_values.geolocation": 1,
            "profile.default_content_setting_values.notifications": 1
        })

        chrome_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'chromedriver.exe')
        self.cam_browser = webdriver.Chrome(chrome_path, chrome_options=opt)
        self.cam_browser.get('http://localhost:5000/cam')

        self.game_browser = webdriver.Chrome(chrome_path)
        self.game_browser.get('http://localhost:5000/game')

        print("[*] Initializing Chrome browser")

    def run(self):
        self.init_server()
        self.init_browser()


if __name__ == '__main__':
    app = App()
    Server.jump_function = jump
    app.run()
