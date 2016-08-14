# DHT11

![DHT11 connected to a Raspberry Pi 3 Model B](https://github.com/marcheiligers/piscripts/blob/master/dht11/rpi3b_dht11.png?raw=true)

The two examples here are based roughly on [the code found on UUGear](http://www.uugear.com/portfolio/dht11-humidity-temperature-sensor-module/).

The DHT11 sets the GPIO pin to LOW between bits. It will then set the pin to HIGH for 26 to 28µs for a 0 bit and 70µs for a 1 bit. Then back to LOW for some period before the next bit is sent. Both these examples essentially read like this but I think that `temp_humid2.py` is much clearer in this (and also turns out to be less code overall).

On my DHT11 I get weird outputs no matter what technique I use to read the device. It's either very badly calibrated or actually broken in some way.

``` bash
pi@raspberrypi:~/piscripts $ sudo python temp_humid2.py
Humidity: 142%, Temparature: 14ºC, Checksum: True (28 <=> 28)
```

I'm in Arizona, In summer. It's certainly not 14ºC. Not even here in my airconditioned home office.

## Update

The set up has gotten a little fancier and the code has been updated to match more closely with the explanation [found here on RPiBlog](http://www.rpiblog.com/2012/11/interfacing-temperature-and-humidity.html)

![RPiBlog Timing Diagram](http://1.bp.blogspot.com/-_sMwYSZMGLw/UJpY2RYIA9I/AAAAAAAAAS0/rJ9ZQwZ3IfM/s1600/DHT11+timing+diagram.jpg)

Following that timing diagram, `temp_humid2.py` now sets a LOW signal for 20ms followed by a HIGH for 2µs and then switches straight into reading and ignoring a LOW followed by a HIGH which signals the start of the incoming data. Using this I was able to get accurate results and checksums that matched most of the time. Occassionally it hangs in one of the loops, presumably because the Python code was interuppted by the OS task scheduler and it missed the entire message, or at least enough of it to end up in an infinite loop. Unfortunately adding additional code for timeouts makes the situation much, much worse. While it will occassionally succeed, most reads fail. It seems to me that Python is simply too slow to be able to do the additional timeout checks in time. This surprises me somewhat, but there you go.

![DHT11 now connected with a Canakit connector](https://github.com/marcheiligers/piscripts/blob/master/dht11/rpi3b_canakit_dht11.png?raw=true)

The resistor in this picture doesn't seem to make much difference.

``` bash
pi@raspberrypi:~/piscripts/dht11 $ sudo python temp_humid2.py
Humidity: 16%, Temparature: 39ºC, Checksum: True (55 <=> 55)
```

That's more like the Arizona I know!