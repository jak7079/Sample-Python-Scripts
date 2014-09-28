Sample-Python-Scripts
=====================

This is a repository of sample Python scripts

<b>LibraryInfo.py</b>:  This script downloads the html code that lists the Columbia University libraries, parses the data for library names, extended descriptions (if available), and email addresses, and then prints that data for each library in the terminal.

<b>map_directions.py</b>:  This script prints out directions directions obtained from JSON output of the Google Maps API. It guesses the users origin by finding their IP address and asks the user if they would like directions from the guessed point. If the user does not, the script asks them for a new origination point, a destination, and an optional waypoint. The script then gets querys the <a href="https://developers.google.com/maps/documentation/directions/">Google Maps API</a>, formats the text, and prints out step-by-step directions keeping track of cumulative distance and time. Finally, the script will query the Google Streetview API to download and display an image of the destination if one is available.

<b>msuCSE231proj08.py</b>:  This script is a solution to the MSU CSE 231 problem found at http://bit.ly/YzZdZF. The script reads and parses training data to determine attributes for two classes of wage-earners. The script then reads in exercise data and for each record uses a simple algorithm that compares the record's attirbutes with those in the training set to guess which class the record belongs to, records whether it was correct, and outputs its accuracy to the console.

<b>msuCSE231proj10.py</b>:  This script is a solution to the MSU CSE 231 problem found at http://bit.ly/1pzV5PC. It uses various classes to simulate an elevator responding to passenger calls. The user inputs the number of passengers and the number of floors in the building. The script then creates Building, Elevator, and Passenger objects based on the input data. The program randomly assigns origin and destination floors to each passenger. The elevator the goes from floor 1 to pick each passenger up, recording when they get on, when they get off, how many passengers are riding the elevator at any time, and whether a passenger's journey is completed.
