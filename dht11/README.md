# DHT11

![DHT11 connected to a Raspberry Pi 3 Model B](https://www.evernote.com/l/ABhQatj2l0lOqKzuuu69QBd-MQ_OH3ZGoEA)

The two examples here are based roughly on [the code found on UUGear](http://www.uugear.com/portfolio/dht11-humidity-temperature-sensor-module/).

The DHT11 sets the GPIO pin to LOW between bits. It will then set the pin to HIGH for 26 to 28µs for a 0 bit and 70µs for a 1 bit. Then back to LOW for some period before the next bit is sent. Both these examples essentially read like this but I think that `temp_humid2.py` is much clearer in this (and also turns out to be less code overall).

On my DHT11 I get weird outputs no matter what technique I use to read the device. It's either very badly calibrated or actually broken in some way.

``` bash
pi@raspberrypi:~/piscripts $ sudo python temp_humid2.py
Humidity: 142%, Temparature: 14ºC, Checksum: True (28 <=> 28)
```

I'm in Arizona, In summer. It's certainly not 14ºC. Not even here in my airconditioned home office.