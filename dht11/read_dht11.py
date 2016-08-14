#!/usr/bin/python
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time
from interruptingcow import timeout

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

def read_humidity_and_temp(attempts = 5):
   try:
      with timeout(1, exception=RuntimeError):
         init_comms()
         bits = read_bits()
         humidity = bits_to_byte(bits[0:8])
         other1 = bits_to_byte(bits[8:16])
         temperature = bits_to_byte(bits[16:24])
         other2 = bits_to_byte(bits[24:32])
         checksum = bits_to_byte(bits[32:40])
         compared = (humidity + temperature + other1 + other2) & 0xFF
         if checksum != compared:
            raise RuntimeError("Checksum does not match")
         return (humidity, temperature)
   except RuntimeError:
      if attempts > 0:
         time.sleep(0.2)
         return read_humidity_and_temp(attempts - 1)
      else:
         raise

if __name__ == "__main__":
   humidity, temperature = read_humidity_and_temp()
   print "Humidity: {}%, Temparature: {}ºC".format(humidity, temperature)


