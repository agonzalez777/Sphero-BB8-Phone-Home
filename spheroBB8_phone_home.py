import urllib2
import requests
from datetime import datetime
import json
from math import radians, cos, sin, atan2, degrees, asin, sqrt
import time
import sys
import BB8_driver
import pytz

iss_pass_url = "http://api.open-notify.org/iss-pass.json"
iss_now_url = "http://api.open-notify.org/iss-now.json"

def calculate_initial_compass_bearing(pointA, pointB):
    """
    Code From: https://gist.github.com/jeromer/2005586#file-compassbearing-py

    Calculates the bearing between two points.

    :Parameters:
      - `pointA: The tuple representing the latitude/longitude for the
        first point. Latitude and longitude must be in decimal degrees
      - `pointB: The tuple representing the latitude/longitude for the
        second point. Latitude and longitude must be in decimal degrees

    :Returns:
      The bearing in degrees

    :Returns Type:
      float
    """
    if (type(pointA) != tuple) or (type(pointB) != tuple):
        raise TypeError("Only tuples are supported as arguments")

    lat1 = radians(pointA[0])
    lat2 = radians(pointB[0])

    diffLong = radians(pointB[1] - pointA[1])

    x = sin(diffLong) * cos(lat2)
    y = (cos(lat1) * sin(lat2)) - ((sin(lat1)
            * cos(lat2) * cos(diffLong)))

    initial_bearing = atan2(x, y)

    # Now we have the initial bearing but math.atan2 return values
    # from -180 to +180 which is not what we want for a compass bearing
    # The solution is to normalize the initial bearing as shown below
    initial_bearing = degrees(initial_bearing)
    compass_bearing = (initial_bearing + 360) % 360

    return compass_bearing

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    km = 6367 * c
    return km * 0.621371

def nextPass(lat,long):
    # Returns the number of seconds till the ISS will next pass a given lat,long
    response = requests.get(iss_pass_url, params={'lat': lat, 'lon': long}).json()
    if 'response' in response:
        dur = response['response'][0]['duration']
        pass_datetime = datetime.fromtimestamp(response['response'][0]['risetime'], tz=pytz.utc)
        print dur
        return [((pass_datetime - datetime.now(tz=pytz.utc)).total_seconds()), dur]

def distanceAndBearingToISS(lat,long):
    # Returns the number of miles between the ISS's Lat/Long and a given lat long
    obj = json.loads(urllib2.urlopen(iss_now_url).read().decode('utf8'))
    iss_lat = obj['iss_position']['latitude']
    iss_long = obj['iss_position']['longitude']
    return [haversine(float(long), float(lat), float(iss_long), float(iss_lat)), int(calculate_initial_compass_bearing((lat,long),(float(iss_lat),float(iss_long))))]



if __name__ == "__main__":

    if len(sys.argv) < 4:
        print "Incorrect Number of Parameters: Require [BB-8 MAC Address] [Current_Lat] [Current_Long]"
        sys.exit(1)

    current_lat = float(sys.argv[2])
    current_long = float(sys.argv[3])

    bb8 = BB8_driver.Sphero(deviceAddress=sys.argv[1])
    bb8.connect()

    # Set Current Heading (Should be pointed due north)
    bb8.set_heading(0,False)

    duration_end = 0
    while True:
        try:
            print('{} seconds left till next pass!'.format(nextPass(current_lat,current_long)[0]))
            [distance,bearing] = distanceAndBearingToISS(current_lat,current_long)
            print "Distance from BB-8", distance, "and bearing", bearing
            # Move BB-8 Head towards that heading
            bb8.roll(0, int(bearing),0,False)
            if (time.time() <= duration_end):
                bb8.set_rgb_led(255, 0, 0, 0, False)
                # print ("RED - rgb (255,0,0)", distance)
            elif (distance > 10375):
                bb8.set_rgb_led(255, 0, 255, 0, False)
                #print ("VIOLET -  rgb(238,130,238)", distance)
            elif (distance <= 10375 and distance > 8300):
                bb8.set_rgb_led(0, 0, 255, 0, False)
                #print ("BLUE   -  rgb(0,0,255)", distance)
            elif (distance <= 8300 and distance > 6225):
                bb8.set_rgb_led(0, 255, 0, 0, False)
                #print ("GREEN - rgb (0,255,0)", distance)
            elif (distance <= 6225 and distance > 4150):
                bb8.set_rgb_led(255, 255, 0, 0, False)
                #print ("YELLOW - rgb (255,255,0)", distance)
            else:
                bb8.set_rgb_led(255, 165, 0, 0, False)
                #print ("ORANGE - rgb (255,165,0)", distance)


            #BB-8 flashes when it is less then 2 minutes before pass time
            [seconds,duration] = nextPass(current_lat, current_long)
            if (seconds > 0 and seconds < 120):
                t_end = time.time() + seconds
                while time.time() < t_end:
                    bb8.set_rgb_led(255, 0, 255, 0, False)
                    bb8.set_rgb_led(0, 0, 255, 0, False)
                    bb8.set_rgb_led(0, 255, 0, 0, False)
                    bb8.set_rgb_led(255, 255, 0, 0, False)
                    bb8.set_rgb_led(255, 0, 255, 0, False)
                    bb8.set_rgb_led(255, 165, 0, 0, False)
                    bb8.set_rgb_led(255, 0, 0, 0, False)
                duration_end = time.time() + duration
            time.sleep(5)

        except KeyboardInterrupt:
            bb8.disconnect()
            sys.exit(0)




