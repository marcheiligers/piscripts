import os
import json
import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime

def post_to_pilog(data):
  url = "https://pilog.herokuapp.com/logs"
  headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
  usn, pwd = os.environ["PILOG_AUTH"].split(":")
  auth = HTTPBasicAuth(usn, pwd)
  content = { 'content': data }
  resp = requests.post(url, data=json.dumps(content), headers=headers, auth=auth)
  log_response(resp)
  return resp

def log_response(resp):
  log(resp.text)

def log(message):
  with open('pilog.log', 'a') as f:
    f.write("{0}: {1}\n".format(datetime.now().isoformat(), message))
