from pyonep import onep
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


###############################################################
### Main Code #################################################
###############################################################

o = onep.OnepV1()
cik = '455954b2b6e787bc71fad187e4471f51700fb191'

# Define Resource IDs. These taken from Exosite portal
Internal_temperature_ID = 'a51ea54054f6022c358e864754b7d7a5248f2882'
Internal_pressure_ID    = 'cc34f7c02f9e34d16d7d267ae96369673ff13996'
Internal_humidity_ID    = 'fa31fa50c9c26bbbd07ba6ca320b2b71bc8dc024'
Heading_ID              = '182fb79e005f000f5684e483386556ea691786d7'

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
        

        # If data has been sent successfully, empty the on-boad log file.
        if "ok" in result:
            print "OK"
            open(Log_filename,'w').close()        
        
    else:
        print "EMPTY - No Data to send!"
            


