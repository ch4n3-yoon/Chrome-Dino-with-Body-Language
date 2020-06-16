
import os
import re


blacklists = [ 'kakaotalk', 'slack', 'naver.line', 'telegram', 'trillian', 'aim', 'pidgin', 'paltalk', 'digsby',
        'facebook', 'messenger', 'icq', 'miranda', 'chrome', 'firefox', 'safari', 'whale', 'mail', 'outlook',
        'thunderbird', 'onedrive', 'backup and sync', 'dropbox', 'skype', 'iexplore', 'edge', 'icloud', 'line.exe',
        'webex' ]

tasklist = [task.strip() for task in os.popen('tasklist').readlines()]

p = []
for task in tasklist:
    m = re.match("(.+?) +(\d+) (.+?) +(\d+) +(\d+.* K).*", str(task))
    if m is not None:
        process = {"image": m.group(1),
            "pid": m.group(2),
            "session_name": m.group(3),
            "session_num": m.group(4),
            "mem_usage": m.group(5)
        }

        for black in blacklists:
            if process['image'].lower().find(black) > -1:
                print('taskkill /pid {0} /f'.format(process['pid']))
                print(process)
                res = os.popen('taskkill /pid {0} /f'.format(process['pid'])).read()
                print(res)