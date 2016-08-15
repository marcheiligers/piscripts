import socket
from pilog import *

def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]


ip = get_ip_address()
r = post_log("ip={0}".format(ip))
