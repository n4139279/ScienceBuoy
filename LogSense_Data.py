from sense_hat import SenseHat

sense = SenseHat()

# Measure Internal Temperature
internal_temperature = sense.get_temperature()

# Measure Internal Air Pressure
internal_pressure = sense.get_pressure()

# Measure Internal Humidity
internal_humidity = sense.get_humidity()

# Get Heading
heading = sense.get_compass()

#display results:
print "Temperature: ", internal_temperature
print "Pressure: ", internal_pressure
print "Humidity: ", internal_humidity
print "Heading: ", heading
