
import gps
import subprocess
from subprocess import call
from squid import *
import time
import sys

rgb = Squid(16, 20, 21)

# Listen on port 2947 (gpsd) of localhost
session = gps.gps("localhost", "2947")
session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)

while True:
    try:
        report = session.next()
                # Wait for a 'TPV' report and display the current time
                # To see all report data, uncomment the line below
        print report
        if report['class'] == 'TPV':
            if hasattr(report, 'mode'):
#                print report.mode
#		print report
                if report.mode == 1:
                    rgb.set_color(RED)
                if report.mode > 1:
                    rgb.set_color(BLUE)
                    time.sleep(5)
                    rgb.set_color(OFF)
                    break
    except KeyError:
                pass
    except KeyboardInterrupt:
                quit()
    except StopIteration:
                session = None
                print "GPSD has terminated"

subprocess.Popen(["sudo", "python", "/home/pi/gpslog.py"])
subprocess.Popen(["sudo", "gpspipe", "-r", "-odata.nmea"], shell=False)
sys.exit()


