#!/usr/bin/python
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time

GPIO_DATA_PIN = 4

def init_comms():
   GPIO.setmode(GPIO.BCM)

   GPIO.setup(GPIO_DATA_PIN, GPIO.OUT, initial=GPIO.LOW)
   time.sleep(0.02)
   GPIO.output(GPIO_DATA_PIN, GPIO.HIGH)
   time.sleep(0.000002)
   GPIO.setup(GPIO_DATA_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def read_bits(bit_count = 40, min_high_bit_length = 50): #µs
   bits = []

   while GPIO.input(GPIO_DATA_PIN) == 0:
      pass
   while GPIO.input(GPIO_DATA_PIN) == 1:
      pass

   while len(bits) < bit_count:
      while GPIO.input(GPIO_DATA_PIN) == 0:
         pass
      start = time.time()
      while GPIO.input(GPIO_DATA_PIN) == 1:
         pass
      stop = time.time()

      if (stop - start) * 1000000 > min_high_bit_length:
         bits.append(1)
      else:
         bits.append(0)

   return bits

def bits_to_byte(bits):
   return int("".join(map(str, bits)), 2)


init_comms()
bits = read_bits()
humidity = bits_to_byte(bits[0:8])
other1 = bits_to_byte(bits[8:16])
temperature = bits_to_byte(bits[16:24])
other2 = bits_to_byte(bits[24:32])
checksum = bits_to_byte(bits[32:40])
compared = (humidity + temperature + other1 + other2) & 0xFF

print "Humidity: {}%, Temparature: {}ºC, Checksum: {} ({} <=> {})".format(humidity, temperature, checksum == compared, checksum, compared)
print "\n\n"


