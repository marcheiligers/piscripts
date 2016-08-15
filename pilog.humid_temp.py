import socket
from pilog import *
from dht11 import *

humidity, temperature = read_humidity_and_temp()
post_weather(humidity, temperature)
