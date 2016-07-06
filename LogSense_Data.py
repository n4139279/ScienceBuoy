import csv
import sys
import time

from sense_hat import SenseHat

sense = SenseHat()
# Get time right now
#--todo
current_time = time.time()

# Measure Internal Temperature
internal_temperature = round(sense.get_temperature(),2)

# Measure Internal Air Pressure
internal_pressure = round(sense.get_pressure(),2)

# Measure Internal Humidity
internal_humidity = round(sense.get_humidity(),2)

# Get Heading
heading = round(sense.get_compass(),2)

#display results:
print "Temperature: ", internal_temperature
print "Pressure: ", internal_pressure
print "Humidity: ", internal_humidity
print "Heading: ", heading

# Write the results to a log file along with a timestamp,
# in the following format:
#
# | Timestamp | internal_temperature | internal_pressure | internal_humidity | heading
#
#
# This code opens the file and appends the current data to the bottom of the file

try:
    with open('ScienceBuoyDataLog.csv', 'a') as csvfile:
        writefile = csv.writer(csvfile, delimiter=',')
        response = writefile.writerow( (current_time,
                      internal_temperature,
                      internal_pressure,
                      internal_humidity,
                      heading))


except:
        print "Failed to write"
        print response
finally:
    csvfile.close()
    
                      
