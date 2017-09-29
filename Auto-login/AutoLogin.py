__author__ = 'Ujjwal'

import subprocess
import urllib.request
import urllib.parse
import random
from bs4 import BeautifulSoup
from datetime import datetime
import sys
import socket

socket.setdefaulttimeout(10)

if ('VIT2.4G' in str(subprocess.check_output("netsh wlan show interfaces"))
    or 'VIT5G' in str(subprocess.check_output("netsh wlan show interfaces"))
    or 'VOLSBB' in str(subprocess.check_output("netsh wlan show interfaces"))):
    pass
else:
    exit()

with open(r'password.txt', 'r') as f:
    passwords = f.readlines()

url = 'http://phc.prontonetworks.com/cgi-bin/authlogin?'


class LoginError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


def main(flag):
    while True:
        try:
            x = random.randrange(len(passwords))
            credentials = passwords[x].strip()
            credentials = credentials.split('::')
            print(credentials[0], credentials[1])
            values = {'userId': credentials[0], 'password': credentials[1], 'serviceName': 'ProntoAuthentication', 'Submit22': 'Login'}
            data = urllib.parse.urlencode(values)
            data = data.encode('utf-8')
            req = urllib.request.Request(url, data)
            resp = urllib.request.urlopen(req)
            respData = resp.read()
            soup = BeautifulSoup(respData, "html.parser")
            chk = soup.find_all('p')
            chk2 = soup.find_all('b')
            if not ("Congratulations" in str(chk) or "You are already logged in" in str(chk2)):
                raise LoginError('Not logged in. Trying again.')
            if not flag:
                break
        except LoginError as e:
            print(e.value)

    if ("You are already logged in" not in str(chk2)):
        now = datetime.now()
        t = now.strftime("%d/%m/%Y %I:%M %p")
        with open(r'log.txt', 'a') as f:
            f.write(credentials[0] + "::" + credentials[1] + " " + t + "\n")



if __name__ == '__main__':
    main(0)
    try:
        if sys.argv[1] == 'r':
            main(1)
    except:
        pass
