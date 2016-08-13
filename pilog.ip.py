import os
import socket
import json
import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime

def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

def post_to_pilog(data):
  url = "https://pilog.herokuapp.com/logs"
  headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
  usn, pwd = os.environ["PILOG_AUTH"].split(":")
  auth = HTTPBasicAuth(usn, pwd)
  req = requests.post(url, data=json.dumps(data), headers=headers, auth=auth)
  return req

def log_result(r):
  with open('pilog.ip.log', 'a') as f:
    f.write("{0}: {1}\n".format(datetime.now().isoformat(), r.text))

ip = get_ip_address()
r = post_to_pilog({ 'content': "ip={0}".format(ip) })
log_result(r)