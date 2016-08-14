#!/usr/bin/python
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time

DATA_MAX = 6000

def init_comms():
   GPIO.setmode(GPIO.BCM)

   GPIO.setup(4,GPIO.OUT)
   GPIO.output(4,GPIO.HIGH)
   time.sleep(0.05)
   GPIO.output(4,GPIO.LOW)
   time.sleep(0.01)

   GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def capture_pin():
   data = []

   start_time = time.time()
   for i in range(0, DATA_MAX):
       data.append(GPIO.input(4))
   stop_time = time.time()

   return ((stop_time - start_time) * 1000, data)

def bin2dec(string_num):
    return int(str(int(string_num, 2)))

def drop(data, val):
   while data[0] == val:
      data.pop(0)

def count(data, val):
   length = 0

   while data[0] == val:
      length = length + 1
      data.pop(0)

   return length


def read_byte(data, min_high_bit_length):
   byte = []
   for i in range(0, 8):
      drop(data, 0)
      length = count(data, 1)

      if length > min_high_bit_length:
         byte.append("1")
      else:
         byte.append("0")

   return bin2dec("".join(byte))


init_comms()
ms, data = capture_pin()
read_length = ms / float(DATA_MAX) * 1000.
low_bit_length = int(28 / read_length)
min_high_bit_length = low_bit_length * 1.5
drop(data, 1)
humidity = read_byte(data, min_high_bit_length)
read_byte(data, min_high_bit_length)
temperature = read_byte(data, min_high_bit_length)
read_byte(data, min_high_bit_length)
checksum = read_byte(data, min_high_bit_length)
compared = (humidity + temperature) & 0xFF

print "{} reads captured in {:.3}ms, {:.3}µs per read, ~low bit length {}, min high bit length {}".format(DATA_MAX, ms, read_length, low_bit_length, min_high_bit_length)
print "Humidity: {}%, Temparature: {}ºC, CRC: {} ({} <=> {})".format(humidity, temperature, checksum == compared, checksum, compared)
print "\n\n"


