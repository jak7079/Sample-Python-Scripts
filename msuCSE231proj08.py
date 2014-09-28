###############################################################################
# Tasks
# 1 - Create a training set
# 2 - Train a 'dumb' rule-based classifier
# 3 - Create a test set
# 4 - Apply rule-based classifier to test set
# 5 - Report accuracy of classifier
###############################################################################

###############################################################################
# CONSTANTS
# For use as dictionary keys in training/testing sets and sums
# DONE - Do not modify.
###############################################################################
AGE = "Age"
WORKCLASS = "Work-class"
EDUCATIONNUM = "Education-num"
MARITAL = "Marital-status"
OCCUPATION = "Occupation"
RELATIONSHIP = "Relationship"
RACE = "Race"
SEX = "Sex"
CAPITALGAIN = "Capital-gain"
CAPITALLOSS = "Capital-loss"
HOURS = "Hours-per-week"
CLASS = "Class"
PREDICTED = "Predicted Class"

###############################################################################
# 1. Create a training set
# - Read in file
# - Create a dictionary for each line
# - Add this dictionary to a list
#
# makeTrainingSet
# parameters: 
#     - filename: name of the data file containing the training data records
#
# returns: trainingSet: a list of training records (each record is a dict,
#                       that contains attribute values for that record.)
###############################################################################
def makeTrainingSet(filename):
    # DONE - Do not modify.
    trainingSet = []

    fin = open(filename,'r')

    # Read in file
    for line in fin:
        line = line.strip()
        line_list = line.split(',')

        # Create a dictionary for the line
        # ( assigns each attribute of the record (each item in the linelist)
        #   to an element of the dictionary, using the constant keys )
        record = {}
        record[AGE] = float(line_list[0])
        record[WORKCLASS] = line_list[1]
        record[EDUCATIONNUM] = float(line_list[4])
        record[MARITAL] = line_list[5]
        record[OCCUPATION] = line_list[6]
        record[RELATIONSHIP] = line_list[7]
        record[RACE] = line_list[8]
        record[SEX] = line_list[9]
        record[CAPITALGAIN] = float(line_list[10])
        record[CAPITALLOSS] = float(line_list[11])
        record[HOURS] = float(line_list[12])
        record[CLASS] = line_list[14]

        # Add the dictionary to a list
        trainingSet.append(record)        

    fin.close()
    return trainingSet


###############################################################################
# 2. Train 'Dumb' Classifier
# trainClassifier
# parameters:
#     - trainingSet: a list of training records (each record is a dict,
#                     that contains attribute values for that record.)
#
# returns: two dictionaries, one for >50K and the other for <=50K. In each
#          dictionary, if one attribute is categorical, its value should also
#          be a dictionary.
###############################################################################
def trainClassifier(trainingSet):

    # TODO
    
    # A. initialize two dictionaries for sums of attribute values
    #    and initialize record counts
    high_set = dict()
    low_set = dict()
    
    # Counters for records in the higher and lower income sets
    high_count = 0
    low_count = 0
    
    # Initialize numerical attributes to be averaged
    high_age = 0
    low_age = 0
    high_edu = 0
    low_edu = 0
    high_capGain = 0
    low_capGain = 0
    high_capLoss = 0
    low_capLoss = 0
    high_hours = 0
    low_hours = 0
    
    # Initialize categorical attributes
    high_workClass = dict()
    low_workClass = dict()
    high_marital = dict()
    low_marital = dict()
    high_occupation = dict()
    low_occupation = dict()
    high_relationship = dict()
    low_relationship = dict()
    high_race = dict()
    low_race = dict()
    high_sex = dict()
    low_sex = dict()
    
    # B. process each record in the training set
    #    calculating sums and counts as we go

    for item in trainingSet:
        if item['Class'] == '>50K':
            # Calculate values for the higher income set
            
            # Numerical attributes
            high_age += item['Age']
            high_edu += item['Education-num']
            high_capGain += item['Capital-gain']
            high_capLoss += item['Capital-loss']
            high_hours += item['Hours-per-week']
            
            # Categorical attributes
            high_workClass[item['Work-class']] = high_workClass.get(item['Work-class'],0) + 1
            high_marital[item['Marital-status']] = high_marital.get(item['Marital-status'],0) + 1
            high_occupation[item['Occupation']] = high_occupation.get(item['Occupation'],0) + 1
            high_relationship[item['Relationship']] = high_relationship.get(item['Relationship'],0) + 1
            high_race[item['Race']] = high_race.get(item['Race'],0) + 1
            high_sex[item['Sex']] = high_sex.get(item['Sex'],0) + 1
            
            high_count += 1
        else:
            # Calculate values for the lower income set
            
            # Numerical attributes
            low_age += item['Age']
            low_edu += item['Education-num']
            low_capGain += item['Capital-gain']
            low_capLoss += item['Capital-loss']
            low_hours += item['Hours-per-week']
            
            # Categorical attributes
            low_workClass[item['Work-class']] = low_workClass.get(item['Work-class'],0) + 1
            low_marital[item['Marital-status']] = low_marital.get(item['Marital-status'],0) + 1
            low_occupation[item['Occupation']] = low_occupation.get(item['Occupation'],0) + 1
            low_relationship[item['Relationship']] = low_relationship.get(item['Relationship'],0) + 1
            low_race[item['Race']] = low_race.get(item['Race'],0) + 1
            low_sex[item['Sex']] = low_sex.get(item['Sex'],0) + 1
            
            low_count += 1
           
       
    # C. calculate averages for continuous attributes, and
    #    calcuate ratios of category for categorical attributes
    high_set = calc_set_avs(high_age, high_edu, high_capGain, high_capLoss, high_hours, high_workClass,
               high_marital, high_occupation, high_relationship, high_race, high_sex, high_count)

    low_set = calc_set_avs(low_age, low_edu, low_capGain, low_capLoss, low_hours, low_workClass,
              low_marital, low_occupation, low_relationship, low_race, low_sex, low_count)
    
    
    # return the two dictionaries
    return (high_set, low_set)

def calc_set_avs(age, edu, capGain, capLoss, hours, workClass, marital, occupation, relationship, race, sex, count):
    # Calculate the average values for a given set
    set = dict()
    
    # Categorical averages
    set['avg_age'] = float(age)/count
    set['avg_edu'] = float(edu)/count
    set['avg_capGain'] = float(capGain)/count
    set['avg_capLoss'] = float(capLoss)/count
    set['avg_hours'] = float(hours)/count
    
    
    for item in workClass:
        workClass[item] = float(workClass[item])/count
    set['workClass_dist'] = workClass
    
    for item in marital:
        marital[item] = float(marital[item])/count
    set['marital_dist'] = marital
    
    for item in occupation:
        occupation[item] = float(occupation[item])/count
    set['occupation_dist'] = occupation
    
    for item in relationship:
        relationship[item] = float(relationship[item])/count
    set['relationship_dist'] = relationship
    
    for item in race:
        race[item] = float(race[item])/count
    set['race_dist'] = race
    
    for item in sex:
        sex[item] = float(sex[item])/count
    set['sex_dist'] = sex
    
    return set
    
###############################################################################
# 3. Create a test set
# - Read in file
# - Create a dictionary for each line
# - Initialize each record's predicted class to 'unknown'
# - Add this dictionary to a list
#
# makeTestSet
# parameters: 
#     - filename: name of the data file containing the test data records
#
# returns: testSet: a list of test records (each record is a dict,
#                       that contains attribute values for that record
#                       and where the predicted class is set to 'unknown'. 
###############################################################################
def makeTestSet(filename):

    # DONE - Do not modify.
    testset = makeTrainingSet(filename)

    for record in testset:
        record[PREDICTED] = 'unknown'

    return testset


###############################################################################
# 4. Classify test set
#
# classifyTestRecords
# parameters:
#      - testSet: a list of records in the test set, where each record
#                 is a dictionary containing values for each attribute
#      - dict1: a dictionary for >50K
#      - dict2: a dictionary for <=50K
#
# returns: testSet with the predicted class set to either >50K or <=50K
#
# for each record, if the majority of attributes are closer to dict1,
# then predict the record as >50K
###############################################################################
def classifyTestRecords(testSet, dict1, dict2):
    # TODO
    
    # For each record in testset

        # initialize >50K and <=50K votes to zero

        # for each attribute of the record
            # if attribute value is closer to dict1 then
            # add one to >50K vote. Otherwise, add one to <=50K vote

        # if >50K vote greater than <=50K vote then
        # predicted class of record is >50K (set predicted class value)
        # otherwise, the predicted class is <=50K
            
#    return testSet
    for record in testSet:
        # Initialize counter variables
        higherCount = 0
        lowerCount = 0
    
        # Age Test
        (higherCount, lowerCount) =  numericParamTest('Age', 'avg_age', record, higherCount, lowerCount, dict1, dict2)
                    
        # Education Test
        (higherCount, lowerCount) =  numericParamTest('Education-num', 'avg_edu', record, higherCount, lowerCount, dict1, dict2)
        
        # Capital Gains Test
        (higherCount, lowerCount) =  numericParamTest('Capital-gain', 'avg_capGain', record, higherCount, lowerCount, dict1, dict2)
        
        # Capital Losses Test
        (higherCount, lowerCount) =  numericParamTest('Capital-loss', 'avg_capLoss', record, higherCount, lowerCount, dict1, dict2)
        
        # Hours Worked Test
        (higherCount, lowerCount) =  numericParamTest('Hours-per-week', 'avg_hours', record, higherCount, lowerCount, dict1, dict2)

        
        # Work Class Test
        (higherCount, lowerCount) =  categParamTest('Work-class', 'workClass_dist', record, higherCount, lowerCount, dict1, dict2)
        
        # Marital Status Test
        (higherCount, lowerCount) =  categParamTest('Marital-status', 'marital_dist', record, higherCount, lowerCount, dict1, dict2)
        
        # Occupation
        (higherCount, lowerCount) =  categParamTest('Occupation', 'occupation_dist', record, higherCount, lowerCount, dict1, dict2)
        
        # Relationship Test
        (higherCount, lowerCount) =  categParamTest('Relationship', 'relationship_dist', record, higherCount, lowerCount, dict1, dict2)
        
        # Race Test
        (higherCount, lowerCount) =  categParamTest('Race', 'race_dist', record, higherCount, lowerCount, dict1, dict2)
        
        # Sex Test
        (higherCount, lowerCount) =  categParamTest('Sex', 'sex_dist', record, higherCount, lowerCount, dict1, dict2)
        
        if higherCount > lowerCount:
            record['Predicted Class'] = '>50K'
        else:
            record['Predicted Class'] = '<=50K'
    
    return testSet

    
def numericParamTest(testParam, dictParam, record, higherCount, lowerCount, dict1, dict2):
    import math
    
    # This function uses absolute values to determine whether a parameter is closer to the average value of the 
    # equivalent parameter in dict1 or dict2    
    if math.fabs( record[testParam] - dict1[dictParam] ) < math.fabs( record[testParam] - dict2[dictParam] ):
        higherCount += 1
    elif math.fabs( record[testParam] - dict2[dictParam] ) < math.fabs( record[testParam] - dict1[dictParam] ):
        lowerCount += 1
        
    return (higherCount, lowerCount)
            
            
def categParamTest(testParam, dictParam, record, higherCount, lowerCount, dict1, dict2):    
    # This function uses the dictonaries to determine whether a greater percentage of memebers for a given category 
    # are members of dict1 or dict2   
    try:        
        list1Val = dict1[dictParam][record[testParam]]
    except:
        # Case where a key appears in dict2 but not dict1
        list1Val = 0
    
    try:
        list2Val  = dict2[dictParam][record[testParam]]
    except:
        # Case where a key appears in dict1 but not dict2
        list2Val = 0
        
    if list1Val > list2Val:
        higherCount += 1
    elif list1Val < list2Val:
        lowerCount += 1
        
    return (higherCount, lowerCount)
            
###############################################################################
# 5. Report Accuracy
# reportAccuracy
# parameters:
#      - testSet: a list of records in the test set, where each record
#                 is a dictionary containing values for each attribute
#                 and both the predicted and actual class values are set
#
# returns: None
#
# prints out the number correct / total and accuracy as a percentage
###############################################################################
def reportAccuracy(testSet):
    # TODO

    # For each record in the test set, compare the actual class (CLASS)
    # and the predicted class (PREDICTED) to calculate a count of correctly
    # classified records.  Use this to calculate accuracy.
    
    correctRecord = 0
    for item in testSet:
        if item['Predicted Class'] == item['Class']:
            correctRecord += 1
            
    results = float(correctRecord*10000/len(testSet))/100
    print correctRecord, 'correct records out of', len(testSet), 'total records'
    print 'Program accuracy is ' + str(results) + '%'
    
###############################################################################
# main - starts the program
###############################################################################
def main():
    # TODO
    print "Reading in training data..."
    trainingSet = []
    trainingFile = "C:\\Users\\James\\Desktop\\Python\\annual-income-training.data"
    trainingSet = makeTrainingSet(trainingFile)
    print "Done reading training data.\n"

    print "Training classifier..."    
    (high_set, low_set) = trainClassifier(trainingSet)
    print "Done training classifier.\n"

    print "Reading in test data..."
    testFile = "C:\\Users\\James\\Desktop\\Python\\annual-income-test.data"
    testSet = makeTestSet(testFile)
    print "Done reading test data.\n"

    print "Classifying records..."
    testSet = classifyTestRecords(testSet, high_set, low_set)
    print "Done classifying.\n"

    reportAccuracy(testSet)

    print "Program finished."
    
main()
