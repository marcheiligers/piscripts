import os
import json
import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime

# PILOG_URL = "http://127.0.0.1:3000/"
PILOG_URL = "https://pilog.herokuapp.com/"

def post_to_pilog(path, body):
  url = "{}{}".format(PILOG_URL, path)
  headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
  usn, pwd = os.environ["PILOG_AUTH"].split(":")
  auth = HTTPBasicAuth(usn, pwd)
  resp = requests.post(url, data=json.dumps(body), headers=headers, auth=auth)
  log_response(resp)
  return resp

def post_log(data):
  return post_to_pilog("logs", { 'content': data })

def post_weather(humidity, temperature, sensor="RPi", location="Office"):
  body = {
    'location': location,
    'sensor': sensor,
    'humidity': humidity,
    'temperature': temperature
  }
  return post_to_pilog("weathers", body)

def log_response(resp):
  log(resp.text)

def log(message):
  with open('pilog.log', 'a') as f:
    f.write("{0}: {1}\n".format(datetime.now().isoformat(), message))
