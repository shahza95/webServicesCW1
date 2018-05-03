from clientController import *
import sys

bookingNum = ""
chosenPayProviderId = ""

def main():
    while True:
        input = raw_input("Enter your command (to see a list, type: help): ")
        if input == 'findflight':
            findFlightAction()
        if input == 'bookflight':
            bookFlightAction()
        if input == 'paymentmethods':
            paymentMethodsAction()
        if input == 'payforbooking':
            payForBookingAction()
        if input == 'bookingstatus':
            bookingStatusAction()
        if input == 'cancelbooking':
            cancelBookingAction()
        if input == 'help':
            helpAction()
        if input == 'exit':
            exitAction()

def findFlightAction():
    #get departure, destination, date, # of passengers & is flex details
    depAirport = raw_input("Enter departure airport: ")
    destAirport = raw_input("Enter destination airport: ")
    depDate = raw_input("Enter departure date (yyyy-mm-dd): ")
    numPassengers = input("Enter number of passengers: ")
    flex = input("Is the departure date flexible? (True/False): ")
    #call clientController
    flights = findFlight(depAirport, destAirport, depDate, numPassengers, flex)
    print("Found the following flights:")
    for flight in flights['flights']:
        print (flight["flight_num"] + " - " + flight["dep_airport"] + " to " + flight["dest_airport"] + ", departure: " + flight["dep_datetime"] + ", arrival: " + flight["arr_datetime"] + ", price per seat: " + unichr(163) + str(flight["price"]))
    bookFlightAction()


def bookFlightAction():
    #get flight number & passenger details
    flightNumber = raw_input("Enter flight number: ")
    numPassengers = input("Enter number of passengers: ")

    #Get details for every passenger
    passengers = []
    for i in range(numPassengers):
        print("Enter details for passenger " + str(i + 1) + "...")
        firstName = raw_input("First name: ")
        surname = raw_input("Surname: ")
        email = raw_input("Email: ")
        phoneNumber = raw_input("Phone number: ")

        passengers.append({'first_name' : firstName, 'surname' : surname, 'email': email, 'phone': phoneNumber})

    #Call controller
    booking = bookFlight(flightNumber, passengers)
    global bookingNum
    bookingNum = booking['booking_num']

    paymentMethodsAction()

def paymentMethodsAction():
    #Call controller
    paymentMethods()
    #Ask user to choose
    global chosenPayProviderId
    chosenPayProviderId = raw_input("Enter chosen payment provider id: ")
    global bookingNum
    if(bookingNum == ""):
        bookingNum = raw_input("Enter booking number to pay for: ")
    payForBookingAction()

def payForBookingAction():
    #get required parameters from user
    global bookingNum
    global chosenPayProviderId
    if(bookingNum == ""):
        bookingNum = raw_input("Enter booking number: ")
    if(chosenPayProviderId == ""):
        chosenPayProviderId = raw_input("Enter payment provider id: ")
    #call controller to create invoice & pay invoice
    payForBooking(bookingNum, chosenPayProviderId)

def bookingStatusAction():
    #user input for booking number
    bookingNumber = raw_input("Enter booking number: ")
    #call controller to handle request
    bookingStatus(bookingNumber)

def cancelBookingAction():
    #user input for booking number
    bookingNumber = raw_input("Enter booking number: ")
    #call controller to handle request
    cancelBooking(bookingNumber)

def helpAction():
    #list possible accepted commands to client
    print("Possible accepted commands: ")

    print("help            - view list of acceptable commands")
    print("exit            - quit client")
    print("findflight      - search for flights")
    print("bookflight      - make a booking")
    print("paymentmethods  - view and choose a payment method")
    print("payforbooking   - complete booking process through payment")
    print("bookingstatus   - view booking details")
    print("cancelbooking   - cancel a booking")

def exitAction():
    print("Goodbye")
    #shut down client
    sys.exit(0)

if __name__ == "__main__":
    main()



#How to log into payment provider using session
#from requests import Request, Session
#s = Session()
#url = 'http://georgekom.pythonanywhere.com/api/login/'
#payload = {'username':'ll13s6s', 'password':'password'}
#r = s.post(url, data=payload)
