#! /usr/bin/python
# Written by Dan Mandle http://dan.mandle.me September 2012
# License: GPL 2.0

import os
from gps import *
from time import *
import time
import threading
import json
from collections import OrderedDict
from squid import *
import simplekml
import subprocess

kml = simplekml.Kml()

fo = open("logging.txt", "wb")

gpsd = None #seting the global variable

os.system('clear') #clear the terminal (optional)

rgb = Squid(16, 20, 21)

class GpsPoller(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		global gpsd #bring it in scope
		gpsd = gps(mode=WATCH_ENABLE) #starting the stream of info
		self.current_value = None
		self.running = True #setting the thread running to true

	def run(self):
		global gpsd
		while gpsp.running:
			gpsd.next() #this will continue to loop and grab EACH set of gpsd info to clear the buffer

if __name__ == '__main__':
	gpsp = GpsPoller() # create the thread
	try:
		#with open('data.txt', 'a') as outfile:
		gpsp.start() # start it up
		time.sleep(5)
		while True:
			#It may take a second or two to get good data
			#print gpsd.fix.latitude,', ',gpsd.fix.longitude,'	Time: ',gpsd.utc

			#os.system('clear')

			#print
			#print ' GPS reading'
			#print '----------------------------------------'
			#print 'latitude    ' , gpsd.fix.latitude
			#print 'longitude   ' , gpsd.fix.longitude
			#print 'time utc    ' , gpsd.utc,' + ', gpsd.fix.time
			#print 'altitude (m)' , gpsd.fix.altitude
			#print 'eps         ' , gpsd.fix.eps
			#print 'epx         ' , gpsd.fix.epx
			#print 'epv         ' , gpsd.fix.epv
			#print 'ept         ' , gpsd.fix.ept
			#print 'speed (m/s) ' , gpsd.fix.speed
			#print 'climb       ' , gpsd.fix.climb
			#print 'track       ' , gpsd.fix.track
			#print 'mode        ' , gpsd.fix.mode
			#print
			#print 'sats        ' , gpsd.satellites

			if gpsd.fix.mode == 1:
				rgb.set_color(RED)
				continue
			if gpsd.fix.mode > 1:
				rgb.set_color(BLUE)
				time.sleep(1)
				rgb.set_color(GREEN)

			kml.newpoint(coords=[(gpsd.fix.latitude,gpsd.fix.longitude)])
			kml.save("testpath.kml")

			print gpsd.fix

			d = OrderedDict()
			d['latitude'] = gpsd.fix.latitude
			d['longitude'] = gpsd.fix.longitude
			d['time utc'] = gpsd.fix.time
			d['altitude (m)'] = gpsd.fix.altitude
			d['eps'] = gpsd.fix.eps
			d['epx'] = gpsd.fix.epx
			d['epv'] = gpsd.fix.epv
			d['ept'] = gpsd.fix.ept
			d['speed (m/s)'] = gpsd.fix.speed
			d['climb'] = gpsd.fix.climb
			d['track'] = gpsd.fix.track
			d['mode'] = gpsd.fix.mode
			#print "dump:",json.dumps(d)
			
			fo.write(json.dumps(d)+"\n")
			#with open('data.txt', 'a') as outfile:
			#json.dump(d, fo)
			#time.sleep(1) #set to whatever

	except (KeyboardInterrupt, SystemExit): #when you press ctrl+c
		print "\nKilling Thread..."
		gpsp.running = False
		gpsp.join() # wait for the thread to finish what it's doing
	print "Done.\nExiting."
