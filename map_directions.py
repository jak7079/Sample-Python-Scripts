import urllib, json, re, os, tempfile
from BeautifulSoup import *

# Function for guessing user location based on their IP address
def getIPLocation():
    # Get IP address from ip.jsontest.com website
    data = json.loads(urllib.urlopen("http://ip.jsontest.com/").read())

    # Use geobytes.com website to correlate IP address with a city location
    url = 'http://www.geobytes.com/IpLocator.htm?GetLocation&template=php3.txt&IpAddress=' + str(data["ip"])
    data = urllib.urlopen(url).read()

    # Use BeautifulSoup to parse the returned HTML code
    soup = BeautifulSoup(data)

    # Retrieve all of the meta tags and build a list
    tagDict = dict()
    tags = soup('meta')
    for tag in tags:   
        tagDict[str(tag.get('name', None))] = str(tag.get('content', None))
        
    # Return user location
    if tagDict['country'] == 'United States':
        string = tagDict['city'] + ', ' + tagDict['regioncode']
    else:
        string = tagDict['city'] + ', ' + tagDict['country']
        
    return string

# Function for generating Google Maps query URL from user input
def get_input(origin):
    serviceurl = 'http://maps.googleapis.com/maps/api/directions/json?'
    
    if origin == None:
        # If getIPLocation() was unable to determine a location, ask user for starting point
        origin = raw_input('Enter origin: ')
        while len(origin) < 1:
            origin = raw_input('    Starting point is invalid. Please re-enter your starting point: ')
    else:
        # Ask if user wants to use their IP location as a starting point
        getNewOrigin = raw_input('It looks like you are in ' + origin + '. Use that as the start point? (Y/N): ')
        
        # Ask user to re-enter response is it doesn't begin with 'y' or 'n' 
        while getNewOrigin.lower().startswith('y')==False and getNewOrigin.lower().startswith('n') == False:
            getNewOrigin = raw_input('    Please enter Y or N: Use ' + origin + ' as a starting point?')        
        
        # If user says no, ask them for a new starting location
        if getNewOrigin.lower().startswith('n'):
            origin = raw_input('Enter a new starting point: ')
            while len(origin) < 1:
                origin = raw_input('    Starting point is invalid. Please re-enter your starting point: ')
 
    # Ask user for destination
    destination = raw_input('Enter destination: ')
    while len(destination) < 1:
        destination = raw_input('    Destination is invalid. Please enter your destination: ')
    
    # Ask user for an optional waypoint
    waypoint = raw_input('Optional - Enter a waypoint (Hit enter for none): ')
    
    # Construct query url based on whether waypoint exists of not
    if len(waypoint) > 0:
        url = serviceurl + urllib.urlencode({'origin': origin, 'destination': destination, 'waypoints': waypoint})
    else:
        url = serviceurl + urllib.urlencode({'origin': origin, 'destination': destination})
    
    # Construct Streetview URL
    streetViewURL = 'http://maps.googleapis.com/maps/api/streetview?' + urllib.urlencode({'location': destination, 'size': '600x400'})
    
    # Return query url    
    return url, streetViewURL
        
# Function for getting driving directions from Google Maps service
def getGoogleDirections(url):    
    # Read in JSON response from maps service   
    data = urllib.urlopen(url).read()

    # Parse JSON response
    try: js = json.loads(str(data))
    except: js = None
    if 'status' not in js or js['status'] != 'OK':
        print '==== Failure To Retrieve ===='
        print data
        quit()

    # Initiate a list variable for direction list steps
    stepList = list()
    
    try:
        # Attribute route information to Google
        dataSource = js['routes'][0]['copyrights']                
        
        # Routes with waypoints will have multiple legs, so loop over them
        for legIndex in range(len(js['routes'][0]['legs'])):            
            
            # Step through each leg
            for stepIndex in range(len(js['routes'][0]['legs'][legIndex]['steps'])):
                record = dict()
                
                # Get text directions for each step
                html_str = js['routes'][0]['legs'][legIndex]['steps'][stepIndex]['html_instructions']
                
                # Remove all <html> tags from directions using re.sub()
                html_str = re.sub('<div style="font-size:0.9em">', '\n  (', html_str)
                html_str = re.sub('</div>', ')', html_str)
                html_str = re.sub('<.*?>', '', html_str)                
                record['directions'] = html_str
                
                # Get step duration
                record['text_dur'] = js['routes'][0]['legs'][legIndex]['steps'][stepIndex]['duration']['text']
                record['num_dur'] = js['routes'][0]['legs'][legIndex]['steps'][stepIndex]['duration']['value']
                
                # Get step distance
                record['text_dist'] = js['routes'][0]['legs'][legIndex]['steps'][stepIndex]['distance']['text']
                record['num_dist'] = js['routes'][0]['legs'][legIndex]['steps'][stepIndex]['distance']['value']
                
                # Add record to directions list    
                stepList.append(record)                             
    except:
        print 'Error processing this request'
    
    return stepList, dataSource

# Function for converting seconds into days/hours/minutes format    
def seconds2text(val):
    # Calculate the days, minutes, and hours
    days = int( float(val) / 86400 )
    hours = int( (val - (days * 86400)) / 3600 )
    minutes = int(round( ((val - (days * 86400) - (hours * 3600)) / 60), 0))
        
    if days == 0:
        if hours == 0:
            # If hours == 0, only display minutes
            string = str(minutes) + ' minutes since start'
        else:
            # If days == 0, only display hours and minutes
            string = str(hours) + ' hours, ' + str(minutes) + ' minutes since start'
    else:
        # Display days, hours, and minutes
        string = str(days) + ' days, ' + str(hours) + ' hours, ' + str(minutes) + ' minutes since start'
        
    return string
    
# Print Output
def printOutput(stepList, dataSource): 
    # Initialize variables
    stepCount = 1
    cumMeters = 0
    cumSeconds = 0
    
    # Print out the steps in the direction list
    # Output is in the format: 'Step #: textDirections (stepDistance/stepDuration, cumulativeDistance/cumulativeDuration)'
    print '\n' + dataSource
    
    print '\nDirections:'
    for record in stepList:
        cumMeters += record['num_dist']
        cumSeconds += record['num_dur']
            
        print ('Step ' + str(stepCount) + ': ' + record['directions'] + ' (' + record['text_dist'] + '/' +
               record['text_dur'] + ', ' + str(round(float(cumMeters)/1609.3, 1)) + 'mi/' + seconds2text(cumSeconds) +')')
            
        stepCount += 1    

# Display image of destination from Google Streetview
def loadStreetView(streetViewURL):
    # Get the path to the user's temporary directory
    tempDir = tempfile.gettempdir()   
    
    # Download the image data from Streetview
    picture = urllib.urlopen(streetViewURL).read()
    
    # Display a picture of the destination, if Google has one
    if len(picture) > 10000:
        # Save the image to the temporary directory
        fName = tempDir + '\\EnjoyYourTrip.jpg'    
        fhand = open(fName,"wb")
        fhand.write(picture);
        fhand.close()
    
        # Open the image in the default image viewer
        os.system("start " + fName)
   
# Run Code:
def main():
    # 1. Determine user location
    try:
        origin = getIPLocation()
    except:
        origin = None
    
    # 2. Get user parameters for directions and generate query url
    (url, streetViewURL) = get_input(origin)

    # 3. Query Google maps and generate a list of steps
    (stepList, dataSource) = getGoogleDirections(url)

    # 4. Print output
    try:
        if len(stepList) == 0:
            print 'There was an error processing you request, no data was returned. Please try again.'
        else:
            printOutput(stepList, dataSource)  
    except:
        print 'Sorry, there has been an unknown Error'
        
    # 5. Display a Streetview image of the destination location
    try:
        loadStreetView(streetViewURL)
    except:
        print '\nSorry, there was an error displaying an image of your destination'

main()
