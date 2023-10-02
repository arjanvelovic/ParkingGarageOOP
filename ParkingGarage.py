import os
from datetime import datetime

class ParkingGarage():
    '''
    The ParkingGarage class will have the following attributes.
    -rate: float of the garage hourly rate $/hr, default = $1000/hr
    -tickets: list of ticket numbers, default = [*range(100)]
    -parkingSpaces: int of parkingSpaces, default = 100
    -currentticket: dictionary of containing the following current ticket information 
        -ticketnumber: int of unique ticketnumber, default = None
        -paid: boolean if paid, default = False
        -starttime: time when ticket taken, default = None
        -endtime: time when ticket submitted for payment, default = None
        -price: price of payment default = 0
    -captime: int of capped time, default = 3600 seconds, 1hr
    -capprice: int of capped price after cap time of parking, default = $1000
    '''
    # creating instance attributes
    def __init__(self, rate = 1000.0 , tickets = [*range(100)], parkingSpaces = 100, currentticket = {'ticketnumber':None, 'paid':False, 'starttime': None, 'endtime':None, 'price':0}, captime = 3600, capprice = 1000,):
        self.rate = rate
        self.tickets = tickets
        self.parkingSpaces = parkingSpaces
        self.currentticket = currentticket
        self.captime = captime
        self.capprice = capprice

    # when called  
    def takeTicket(self):
        if self.currentticket['starttime'] != None: #ensures that the ticket has been taken
            self.currentticket['ticketnumber'] = self.tickets.pop() #pops ticketnumber from ticketlist
            self.parkingSpaces -= 1 #removes avaible garage spots by 1

            print(f'your ticket number is {self.currentticket["ticketnumber"]}\n') #prints ticket number to user
        else:
            print('A ticket has not been taken, please take one\n')
    
    def payForParking(self):
        if self.currentticket['endtime'] != None: #ensures that the ticket has placed for payment
            #brute force of endtime and starttime to floats
            endtimeint = (self.currentticket['endtime'].hour*60*60) + (self.currentticket['endtime'].minute*60) + self.currentticket['endtime'].second + (self.currentticket['endtime'].microsecond/100000)
            starttimeint = (self.currentticket['starttime'].hour*60*60) + (self.currentticket['starttime'].minute*60) + self.currentticket['starttime'].second + (self.currentticket['starttime'].microsecond/100000)
            totaltime = endtimeint - starttimeint #time difference for calculations
            if totaltime > self.captime: #if total passes over captime
                self.currentticket['price'] = self.capprice #sets price to cap price once 1hr is reached
            else:
                self.currentticket['price'] = round(self.rate * (totaltime/(60*60)),2) #calculates price based on rate and totaltime

    def leaveGarage(self, userinput):
        self.userinput = userinput
        self.currentticket['price'] -= userinput #subtracts price from userinput
        if round(self.currentticket['price'],2) == 0 or round(self.currentticket['price'],2) < 0:
            # sets paid to true and resets all other currentticket values
            self.currentticket['paid'] = True
            self.tickets.append(self.currentticket['ticketnumber'])
            self.parkingSpaces += 1
            self.currentticket['ticketnumber'] = None
            self.currentticket['starttime'] = None
            self.currentticket['endtime'] = None

            if round(self.currentticket['price'],2) == 0:
                print('Thank you, have a nice day!')
            else:
                print(f'your change is ${round(self.currentticket["price"]*-1,2)}, have a nice day!') #returns price if user has change


#Set attributes of parking garage
ExpensiveGarage = ParkingGarage()

#create function to check if string is a float
def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False

#start of user interface which calls the ParkingGarage class
while True:
    if ExpensiveGarage.currentticket['paid'] == True: #first checks if the ticket has been paid
        break

    question = input('Hello, Welcome to the garage\nPlease select the following options on the number pad:\n1) Take a ticket\n2) Pay for ticket\n3) Cancel\n')
    os.system('cls')
    if question == '1': #for taking ticket
        if ExpensiveGarage.currentticket['starttime'] != None: #checks if user already has a ticket
            print('You already have a ticket please select another option')
        else:
            takeTicketQuestion = ''
            while takeTicketQuestion != '2':
                takeTicketQuestion = input(f'We have an hourly rate of ${ExpensiveGarage.rate} for a parking spot\nWould you like to continute 1)yes 2)no\n')
                os.system('cls')
                if takeTicketQuestion == '1':
                    ExpensiveGarage.currentticket['starttime'] = datetime.now() #sets start time
                    ExpensiveGarage.takeTicket() #calls taketicket method to get ticketnumber
                    break
                elif takeTicketQuestion == '2':
                    print('OK Cheapo\n')
                else:
                    print('That was not a valid input\nPlease try again\n')
    elif question == '2': #for paying for a ticket
        if ExpensiveGarage.currentticket['starttime'] == None: #checks if user has ticket
            print('You do not have a ticket, please take one\n')
        else:
            ExpensiveGarage.currentticket['endtime'] = datetime.now() #sets end time
            ExpensiveGarage.payForParking() #calls payForParking method to get price
            while ExpensiveGarage.currentticket['price'] > 0: #holds user in loop as long as price is greater than $1
                priceinput = input(f'You owe ${round(ExpensiveGarage.currentticket["price"],2)}, please input a payment in the keypad\n')
                os.system('cls')
                if priceinput.isnumeric() or isfloat(priceinput): #checks validity of user input
                    userinput = float(priceinput) #converts to float
                    if userinput < 0: #checks for negative input
                        print('That was not a valid input\nPlease try again\n')
                    else:
                        ExpensiveGarage.leaveGarage(userinput) #calls leaveGarage method with userinput
                else:
                    print('That was not a valid input\nPlease try again\n')

    elif question.lower() == '3':
        if ExpensiveGarage.currentticket['starttime'] != None: #stops user from leaving if ticket is not paid (still has starttime)
            print('You still have an unpaid ticket, please pay\n')
        else:
            print('See you later! Alligator!')
            break
    else:
        print('That was not a valid input\nPlease try again\n')