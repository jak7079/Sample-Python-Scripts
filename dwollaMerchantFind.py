import math, string, urllib, json
from dwolla import DwollaUser, DwollaClientApp

# App Application
key = 'ENTER KEY HERE'
secret = 'ENTER SECRET HERE'

# Ask user for a location of interest
print 'Use this tool to find merchants that accept Dwolla near an address of interest\n'
origin = raw_input('Enter the address: ')
while len(origin) < 1:
    origin = raw_input('    Starting point is invalid. Please re-enter your starting point: ')

# Ask user for the maximum number of results to return           
maxHits = raw_input('Enter the maximum number of results (default is 10): ')
if len(maxHits) < 1:
    maxHits = 10
else:
    while type(maxHits) != int:
        try: 
            # Check to see if input is numeric
            maxHits = float(maxHits)
            if maxHits - int(maxHits) == 0:               
                # If input is an integer, convert to int type
                maxHits = int(maxHits)
            else:
                # Prompt user for integer input
                maxHits = raw_input('    Bad input. Please enter an integer maximum: ')
        except:
            # Prompt user for integer input
            maxHits = raw_input('    Bad input. Please enter an integer maximum: ')

# Use Google Maps Geocode API to generate a lat/lon pair for address
geocodeURL = 'http://maps.googleapis.com/maps/api/geocode/json?' + urllib.urlencode({'address': origin})
data = urllib.urlopen(geocodeURL).read()

# Parse JSON response for lat/lon pair
try: js = json.loads(str(data))
except: js = None
if 'status' not in js or js['status'] != 'OK':
    print '==== Failure To Retrieve ===='
    print data
    quit()
else:
    latVal = js['results'][0]['geometry']['location']['lat']
    lonVal = js['results'][0]['geometry']['location']['lng']

# Query Dwolla for spots near the address            
DwollaClient = DwollaClientApp(key, secret)

radius = 2
spots = DwollaClient.get_nearby_spots(latVal, lonVal, radius, maxHits)

# If there are fewer results than the user-specified maximum, query again over a 
# larger radius
while (len(spots) < maxHits) and (radius < 50):
    radius = radius * 5
    spots = DwollaClient.get_nearby_spots(latVal, lonVal, radius, maxHits)

# Output the results
print('The ' + str(len(spots)) + ' closest spots that accept Dwolla are:\n')
rVal = range(0,len(spots))
for index in rVal:
    # Convert the delta parameter (which seems to be Earth Central Angle in degrees) into miles
    distVal = round( ( (spots[index]['Delta'] * math.pi / 180) * 6378 * 0.62 ), 2)

    print (spots[index]['Name'] + '\n' + string.rstrip(spots[index]['Address'], '\n') + '\n' + spots[index]['City'] +
           ', ' + spots[index]['State'] + '\n' + str(distVal) + ' miles away (as the crow flies)\n') 
    



