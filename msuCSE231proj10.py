import random

class Building:
    '''The BUILDING contains the methods run() and output() and the variables customer_list, num_of_floors, max_floor, and min_floor'''
    # Instantiate a BUILDING object
    def __init__(self, customer_list, num_of_floors):
        self.customer_list = customer_list
        self.num_of_floors = num_of_floors
                
        # Determine the highest floor traveled to on the way up
        max_floor = 0
        for item in self.customer_list:
            if item.dst_floor > max_floor:
                max_floor = item.dst_floor                
            if item.start_floor > max_floor:
                max_floor = item.start_floor
        self.max_floor = max_floor
        
        # Determine the lowest floor traveled to on the way down       
        min_floor = max_floor
        for item in self.customer_list:
            if item.dst_floor < min_floor:
                min_floor = item.dst_floor
        self.min_floor = min_floor
        
        # Instantiate an ELEVATOR object
        self.elevator = Elevator(self.max_floor)
        
    # Print ELEVATOR and PASSENGER status    
    def output(self):
        print '\n'
        print self.elevator.__str__()   
        for item in self.customer_list:
            print item            

    # Update the status of the PASSENGER objects
    def update_status(self):  
        count = 0
        for item in self.customer_list:        
            # Update customer floors only if they are on the elevator
            if item.in_elevator == True:
                self.customer_list[count].cur_floor = self.elevator.cur_floor
            
            # Check to see if a customer is getting on or off the elevator            
            if ( (item.cur_floor == self.elevator.cur_floor) and (item.direction == self.elevator.direction)
               and (item.finished == False) and (item.in_elevator == False) ):
                # If elevator is on the same floor and traveling in the same direction as a customer, add them to the elevator
                self.customer_list[count].in_elevator = True
                self.elevator.register_customer(item.ID)
            elif ( (item.dst_floor == self.elevator.cur_floor) and (item.in_elevator == True) ):
                # If the customer is riding the elevator and reaches the destination floor, remove the customer from the elevator
                self.customer_list[count].in_elevator = False
                self.customer_list[count].finished = True
                self.elevator.cancel_customer(item.ID)
                
            count += 1
    
    # Implement the default elevator logic    
    def run(self):                                        
        # Print the initial status
        self.output()
        self.update_status()
        
        # Print the status after any passengers on the first floor have boarded
        self.output()
        
        step_count = 0
        # Move the elevator up and print the passenger status
        while self.elevator.cur_floor <  self.max_floor:
            self.elevator.move('up')
            self.update_status()
            self.output()
            step_count += 1
        
        # Move the elevator down and print the passenger status        
        while self.elevator.cur_floor >  self.min_floor:
            self.elevator.move('down')
            self.update_status()
            self.output()
            step_count += 1
        
        return step_count
        
class Elevator:
    '''The ELEVATOR class contains the methods move(), register_customer(), and cancel_customer(), and the variables register_list, cur_floor, and direction  '''
    # Instantiate an ELEVATOR object
    def __init__(self, num_of_floors):
        self.num_of_floors = num_of_floors
        self.register_list = list()
        self.cur_floor = 1
        self.direction = 'up'
    
    # Function to pass ELEVATOR object status
    def __str__(self):
        if len(self.register_list) == 1:
            str_desc = ('ELEVATOR is on floor ' + str(self.cur_floor) +  ' with 1 PASSENGER and moving ' + self.direction)
        else:
            str_desc = ('ELEVATOR is on floor ' + str(self.cur_floor) +  ' with ' +  str(len(self.register_list)) 
                        + ' PASSENGERS moving ' + self.direction)
        return str_desc
    
    # Function to move the ELEVATOR object up or down one floor
    def move(self, direction):
        # Move the elevator up one floor
        if (self.cur_floor < self.num_of_floors-1) and direction == 'up':
            self.cur_floor += 1
            self.direction = 'up'
        # If the elevator is on the top floor always move down
        elif (self.cur_floor < self.num_of_floors) and direction == 'up':
            self.cur_floor += 1
            self.direction = 'down'
        # Move the elevator down one floor
        elif self.cur_floor > 2 and direction == 'down':
            self.cur_floor -= 1
            self.direction = 'down'
        # If the elevator is on the bottom floor always move up
        else:
            self.cur_floor -= 1
            self.direction = 'up'
    
    # Function to add a customer to the list of elevator riders
    def register_customer(self, ID):
        self.register_list.append(ID)
    
    # Function to remove a customer from the list of elevator riders
    def cancel_customer(self, ID):
        self.register_list.remove(ID)
        
class Customer:
    '''The CUSTOMER class contains the variables ID, start_floor, dst_floor, cur_floor, in_elevator, direction, and finished '''
    # Instantiate a CUSTOMER object
    def __init__(self, ID, num_of_floors):
        self.ID = ID
        self.start_floor = random.randint(1, num_of_floors)
        self.cur_floor = self.start_floor
        self.in_elevator = False
        self.finished = False
        
        self.dst_floor = random.randint(1, num_of_floors)        
        # Check to make sure that the start and end floors are different
        while self.dst_floor == self.start_floor:
            self.dst_floor = random.randint(1, num_of_floors)

        # Determine the direction the customer is traveling in
        if self.start_floor > self.dst_floor:
            self.direction = 'down'
        else:
            self.direction = 'up'
    
    # Function to pass CUSTOMER object status
    def __str__(self):
        if self.in_elevator == True:        
            on_el_str = ' is on the elevator'
        else:
            on_el_str = ' is not on the elevator'
            
        if self.finished == True:        
            fin_str = ' (Journey is finished)'
        else:
            fin_str = ''        
        
        str_desc = ('CUSTOMER #' +  str(self.ID) + on_el_str + ' and is currently on floor ' + str(self.cur_floor) +
                   ' traveling from floor ' + str(self.start_floor) + ' to ' + str(self.dst_floor) + fin_str)
        return str_desc
       
        
# main() is the function that executes the program    
def main():
    # Prompt user for number of floors in building
    num_of_floors = raw_input('Enter the number of floors in the building: ')    
    # Check to see that number is an integer
    while type(num_of_floors) != int:
        try: 
            # Check to see if input is numeric
            num_of_floors = float(num_of_floors)
            if num_of_floors - int(num_of_floors) == 0:
                if num_of_floors < 2:
                    # Prompt user for integer input
                    num_of_floors = raw_input('    Bad input. Please enter an integer number of floors greater than 2: ')
                else:
                    # If input is an integer, convert to int type
                    num_of_floors = int(num_of_floors)
            else:
                # Prompt user for integer input
                num_of_floors = raw_input('    Bad input. Please enter an integer number of floors: ')
        except:
            # Prompt user for integer input
            num_of_floors = raw_input('    Bad input. Please enter an integer number of floors: ')

    # Prompt user for the number of riders
    num_cust = raw_input('Enter the number of customers using the elevator: ')
    # Check to see that number is an integer
    while type(num_cust) != int:        
        try: 
            # Check to see if input is numeric
            num_cust = float(num_cust)
            if num_cust - int(num_cust) == 0:
                if num_cust < 1:
                    # Prompt user for integer input
                    num_cust = raw_input('    Bad input. Please enter an integer number of customers greater than 0: ')
                else:
                    # If input is an integer, convert to int type
                    num_cust = int(num_cust)
            else:
                # Prompt user for integer input
                num_cust = raw_input('    Bad input. Please enter an integer number of customers: ')
        except:
            # Prompt user for integer input
            num_cust = raw_input('    Bad input. Please enter an integer number of customers: ')
    
    # Create the list of Customer objects
    customer_list = list()
    for item in range(1,num_cust+1):
        customer_list.append( Customer(item, num_of_floors) )    
    
    # Instantiate a Building object and run the elevator
    building = Building(customer_list, num_of_floors)
    
    # Run the elevator
    steps = building.run()
    
    print '\nThe elevator moved', steps, 'times'
    
    
main()
