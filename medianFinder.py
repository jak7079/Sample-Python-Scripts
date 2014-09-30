import random

# Number of machines to simulate
numComputers = 10

# Amount of data on each machine
numVals = 1000000

# Number of times to segment each machine
numSegments = 10



# Function to generate 10 lists of one million random numbers from -100 million to + 100 million
def genList(numComputers, numVals):
    compVal = dict()    
    for item in range(0, numComputers):
        numList = list()
        for val in range (0,numVals):
            numList.append(random.randint(-100000000, 100000000))

        compVal[item] = numList
        
    return compVal
    print('Simulating ' + str(numComputers) + ' machines storing ' + str(numVals) + 
          ' integer values')

    
# Function to explicity find the median value of all of the items on all of the computers
def findExtremes(compVal):
    # Create a list with all of the items
    medianList = list()    
    for item in range(0, len(compVal)):
        medianList.extend(compVal[item])    
    # Sort the list
    medianList.sort()

    # Find and return minimum, maximum, and median list values
    minVal = medianList[0]
    maxVal = medianList[len(medianList)-1]
    medIndex = int(len(medianList)/2)    
    
    return minVal, medianList[medIndex], maxVal


# Determine the maximum and minimum values on all computers by stepping through
# segments of stored values
def findExtremesStep(compVal, numSegments):
    maxVal = 0
    minVal = 0
    count = 0
    totalVal = 0
    for item in range(0, len(compVal)):
        # Break data into smaller chunks
        numEl = len(compVal[item])
        startVal = 0
        step = numEl/numSegments
        # Check to make sure we don't go beyond last element
        if startVal + step >= numEl:
            step = numEl-startVal-1
    
        # For each chunk see what max and min values are
        for val in range(0, numSegments):
            segMax = max(compVal[item][startVal:(startVal + step)])
            if segMax > maxVal:
                maxVal = segMax
        
            segMin = min(compVal[item][startVal:(startVal + step)])
            if segMin < minVal:
                minVal = segMin    
    
            startVal += step
            count += 1
         
        # Total nubmer of elements stored across all computer 
        totalVal += numEl 
        
    return minVal, maxVal, count, totalVal

# Iterate over list segments to find the median values
def findMedian(compVal, minV2, maxV2, numSegments, totalVal):
    # Counter for number of iterations
    loop = 1
    count = 0
    
    # Initial value to sort list against
    checkVal = (minV2 + maxV2) / 2
    # If initial value is too close to zero, extra computations are required
    if abs(checkVal) < 100:
        checkVal = checkVal *10
    lastCheckVal = checkVal
    
    # Index of median value
    medIndex = int(totalVal/2)
    
    # This function segments the list compVal and counts how many values in
    # it are less than checkVal
    def countVals (compVal, checkVal, numSegments):
        # Function used to filter list
        def f(x): return x < checkVal
        count = 0
        
        for item in range(0, len(compVal)):
            numEl = len(compVal[item])
            startVal = 0
            step = numEl/numSegments
            # Check to make sure we don't go beyond last element
            if startVal + step >= numEl:
                step = numEl-startVal-1                        
            
            # Break each list into smaller segments
            for val in range(0, numSegments):
                # Determine how many elements in the list segment are greater
                # than checkVal                
                count += len(filter(f, compVal[item][startVal:(startVal + step)]))                
                startVal += step
                
        return count
        
    def minDif (compVal, checkVal, numSegments, maxV2):
        medVal = 0
        minDif = maxV2
        
        for item in range(0, len(compVal)):
            numEl = len(compVal[item])
            startVal = 0
            step = numEl/numSegments
            # Check to make sure we don't go beyond last element
            if startVal + step >= numEl:
                step = numEl-startVal-1                        
            
            # Break each list into smaller segments
            for val in range(0, numSegments):
                miniSegment = compVal[item][startVal:(startVal + step)]
                # Go item by item through each mini-segment
                for index in miniSegment:
                    if abs(index- checkVal) < minDif:
                        medVal = index
                        minDif = abs(index- checkVal)
                
                startVal += step
        return medVal
    
    # Loop over each list adjusting checkVal with each loop
    factor = 0.75
    while (loop <= 75) and (count != medIndex):
        lastCount = count
        count = countVals (compVal, checkVal, numSegments)                
        
        if (abs(checkVal) < 0.1) and (lastCheckVal < 0):
            checkVal = 5
        elif (abs(checkVal) < 0.1) and (lastCheckVal > 0):
            checkVal = -5
        elif (count < medIndex) and (checkVal > 0):
            # Increase checkVal
            lastCheckVal = checkVal
            checkVal = checkVal * (1 + factor)
        elif (count < medIndex) and (checkVal < 0):
            # Increase checkVal
            lastCheckVal = checkVal
            checkVal = checkVal * (1 - factor)
        elif (count > medIndex) and (checkVal > 0): 
            # Decrease checkVal
            lastCheckVal = checkVal
            checkVal = checkVal * (1 - factor)
        else:
            # Decrease checkVal
            lastCheckVal = checkVal
            checkVal = checkVal * (1 + factor)
        
        # Check to see if you are circling the median value
        if (lastCount > medIndex) and (count < medIndex):
            factor = factor/2
        elif (lastCount < medIndex) and (count > medIndex):
            factor = factor/2
        
        
        print('Loop #' + str(loop) + ': ' + str(count) + ' values are less than guess value of ' +
               str(checkVal) + '. Median index is ' + str(medIndex))
        loop +=1
        
    medVal = minDif (compVal, checkVal, numSegments, maxV2)
    print('\nMedian value is ' + str(medVal))
           
        
def main():
    # Generate the list of random numbers
    print 'Generating random number list...\n'
    compVal = genList(numComputers, numVals)
    
    # Get the statistics for the list
    (minV, medV, maxV) = findExtremes(compVal)
    print 'List minimum:', minV
    print 'List median:', medV
    print 'List maximum:', maxV
    
    
    # Get the statistics by stepping through list in segments
    (minV2, maxV2, counts, totalVal) = findExtremesStep(compVal, numSegments)
    print '\n'
    print 'List minimum:', minV2
    print 'List maximum:', maxV2
    print 'Total elements:', totalVal
    print ('Values calculated over ' + str(counts) + ' steps')
    
    # Try to calculate median
    findMedian(compVal, minV2, maxV2, numSegments, totalVal)
    
    return compVal, minV2, maxV2, counts
    
(compVal, minV2, maxV2, counts) = main()
