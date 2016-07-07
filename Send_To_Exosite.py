from pyonep import onep
from Exosite_cik import *
import os
import pandas
import urllib2

###############################################################
##### Function Defines ########################################
###############################################################


# define function to check if we're connected to the internet
def testConnection():
        try:
                urllib2.urlopen("http://www.google.com").close()
        except urllib2.URLError:
                connection = False
        else:
                connection = True                


# define function to send data to Exosite
def uploadData (_timestamp, _data, _ID, _numrows):
        SendData=[[0 for j in range(2)] for k in range(_numrows)]
    
        for i in range(0,_numrows):
            SendData[i][0]= _timestamp[i]
            SendData[i][1]= _data[i]
            
        result = o.recordbatch(cik,_ID, SendData,defer=False)
        return result

# define function to read data from Exosite
def readSingleExositeValue ( _ID):
        isok, response = o.read( cik, _ID,{'limit': 1, 'sort': 'desc', 'selection': 'all'})
        record = response[0]
        timestamp = record[0]
        value = record[1]
        #print "is ok?", isok
        #print "response: ", response
        #print "KeepAlive: ", value

        return value
	

# define function to shut down pi
def shutdown_pi():
    command = "/usr/bin/sudo /sbin/shutdown now"
    import subprocess
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]
    print output

# Alternative method:	
#	os.system('shutdown now -h')



###############################################################
### Main Code #################################################
###############################################################

o = onep.OnepV1()

## Define Resource IDs. These taken from Exosite portal
## All IDs are imported from Exosite_cik.py to ensure privacy
## of sensitive codes. 
##
# cik = '# Insert CIK #'
# Internal_temperature_ID 	= '# Insert Resource ID #'
# Internal_pressure_ID    	= '# Insert Resource ID #'
# Internal_humidity_ID    	= '# Insert Resource ID #'
# Heading_ID              	= '# Insert Resource ID #'
# LedButton_ID				= '# Insert Resource ID #'
# KeepAliveButton_ID		= '# Insert Resource ID #'

Log_filename = 'ScienceBuoyDataLog.csv'
# Check if the log file exists:
if os.path.isfile(Log_filename):
    file = open(Log_filename);
             
    # Check if there is any data in the log file
    # Make a local copy of the data to prevent
    # corruption if it is written whilst being transmitted
    data = file.readlines()

    numrows = len(data)

    colnames = ('Timestamp',
                'Internal_temperature',
                'Internal_pressure',
                'Internal_humidity',
                'Heading')
    
    if numrows>0:
        # Send that data to exosite

        data = pandas.read_csv(Log_filename, names=colnames)
        print data

        Timestamp = data.Timestamp.tolist()
        Heading = data.Heading.tolist()
        Internal_temperature = data.Internal_temperature.tolist()
        Internal_pressure = data.Internal_pressure.tolist()
        Internal_humidity = data.Internal_humidity.tolist()

        result = uploadData(Timestamp, Internal_temperature, Internal_temperature_ID, numrows)
        result = uploadData(Timestamp, Internal_pressure, Internal_pressure_ID, numrows)
        result = uploadData(Timestamp, Internal_humidity, Internal_humidity_ID, numrows)
        result = uploadData(Timestamp, Heading, Heading_ID, numrows)
        

        # If data has been sent successfully, empty the on-board log file.
        if "ok" in result:
            print "OK"
            open(Log_filename,'w').close()        
        
    else:
        print "EMPTY - No Data to send!"
            
#########
## Now check whether to shut down the raspberry pi 
## or stay alive.
##
## Read the value of KeepAliveButton from exosite
## and if 0 shut down rpi
#########
KeepAlive = readSingleExositeValue (KeepAliveButton_ID)

if KeepAlive == 0:
        shutdown_pi()
