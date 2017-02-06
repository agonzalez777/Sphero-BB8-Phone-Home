Sphero BB8 Phone Home
--------------------

An International Space Station (ISS) Tracker using Sphero's BB-8 Droid in python. 

BB-8 turns different colors (from Purple->Red) depending on how close the ISS is to your horizon. When it starts flashing different colors -- that is the two minute warning to go outside to see the ISS.
 
BB-8's head also turns to the direction of the Satellite (so you know where to look)

> This application adapted jchadwhite's Python Library to control BB-8:  https://github.com/jchadwhite/SpheroBB8-python.git

**System Requirements:**

* **Operating System**: Linux
* **Python Version**: 2.7
* **Python Modules Needed**: bluepy, urllib2, requests


**Usage Instructions:**

1. Use "`$ sudo hcitool lescan`" to find BB8's MAC address
2. Point BB-8 so that BB-8's head is pointing north
2. Run "`./spheroBB8_phone_home.py (Mac Address you obtained from the previous step) (Current Lat) (Current Long)`"
 
***Included Scripts:***

**spheroBB8_phone_home.py**
Main Script

**BB8_driver.py**
BB-8 Driver (imported in spheroBB8_phone_home.py in order to connect to BB-8)
