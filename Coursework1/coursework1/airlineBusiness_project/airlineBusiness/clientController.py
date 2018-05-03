import requests
import json

BASE_URL = "http://ll13s6s.pythonanywhere.com/api/"

#Call backend web service & set up display of data
def findFlight(depAirport, destAirport, depDate, numPassengers, flex):
    payload = {'dep_airport': depAirport, 'dest_airport': destAirport, 'dep_date':depDate, 'num_passengers':numPassengers, 'is_flex':flex}
    response = requests.get(BASE_URL + "findflight/", json=payload)
    if (response.status_code == 200):
        flights = json.loads(response.text)
        return flights
    else:
        print(response.text)

def bookFlight(flightNumber, passengers):
    payload = {'flight_id': flightNumber, 'passengers' : passengers}
    response = requests.post(BASE_URL + "bookflight/", json=payload)
    if (response.status_code == 201):
        booking = json.loads(response.text)

        print("The following booking is on hold:")
        print(booking['booking_num'] + '- status: ' + booking['booking_status'] + ", total price: " + unichr(163) + str(booking['tot_price']) )
        return booking
    else:
        print(response.text)

def bookingStatus(bookingNumber):
    payload = {'booking_num':bookingNumber}
    response = requests.get(BASE_URL + "bookingstatus/", json=payload)
    if (response.status_code == 200):
        booking = json.loads(response.text)
        print(booking['booking_num'] + '- status: ' + booking['booking_status'] + ", flight number: " + booking['flight_num'] + ", departure airport: " + booking['dep_airport'] + ", destination airport: " + booking['dest_airport'] + ", departure date time: " + booking['dep_datetime'] + ", arrival date time: " + booking['arr_datetime'] + ", flight duration: " + booking['duration'] + " hours" )
    else:
        print(response.text)

def cancelBooking(bookingNumber):
    payload = {'booking_num':bookingNumber}
    response = requests.post(BASE_URL + "cancelbooking/", json=payload)
    if (response.status_code == 201):
        result = json.loads(response.text)
        print("Booking successfully cancelled.")
        print(result['booking_num'] + '- status: ' + result['booking_status'])
    else:
        print(response.text)

def paymentMethods():
    response = requests.get(BASE_URL + "paymentmethods/", json={})

    if(response.status_code == 200):
        providers = json.loads(response.text)
        print("The possible payment providers are:")
        for provider in providers['providers']:
            print("ID: " + provider['pay_provider_id'] + " - " + provider['pay_provider_name'])
    else:
        print(response.text)

def payForBooking(bookingNumber, payProviderId):
    payload = {'booking_num' : bookingNumber, 'pay_provider_id': payProviderId}
    response = requests.post(BASE_URL + "payforbooking/", json=payload)
    if(response.status_code == 201):
        fulfilInvoice(json.loads(response.text))
        return response
    else:
        print(response.text)

def fulfilInvoice(invoice):
    #pay invoice
    print(invoice)
    paymentProviderBaseUrl = invoice['url']
    paymentPayload = {'payprovider_ref_num' : invoice['invoice_id'], 'client_ref_num': invoice['booking_num'], 'amount': invoice['amount']}
    session = requests.Session()
    response = session.post(paymentProviderBaseUrl + "payinvoice/", json=paymentPayload)
    #if unauthorised
    #first log in
    if(response.status_code == 401):
        print("Unauthorised. You must log into your account.")
        action = raw_input("Choose register/login: ")
        #if client chooses to register, register with payment provider and open account, deposit money
        if(action == "register"):
            first_name = raw_input("Enter first name: ")
            surname = raw_input("Enter surname: ")
            email = raw_input("Enter email: ")
            phone = raw_input("Enter phone number: ")
            regUsername = raw_input("Enter username: ")
            regPassword = raw_input("Enter password: ")
            registerPayload = {'first_name' : first_name, 'surname' : surname, 'email':email, 'phone':phone, 'username':regUsername, 'password':regPassword, 'customer_type':'personal'}
            response = session.post(paymentProviderBaseUrl + "register/", json=registerPayload)
            #create current account
            if(response.status_code == 201):
                #login
                loginPayload = {'username':regUsername,'password':regPassword}
                loginResponse = session.post(paymentProviderBaseUrl + "login/", data=loginPayload)
                if(loginResponse.status_code == 200):
                    response = session.post(paymentProviderBaseUrl + "newaccount/")
                    if(response.status_code == 201):
                        print("Created current account, with number: " + response.text)
                    else:
                        print(response.text)
                else:
                    print(loginResponse.text)
            else:
                print(response.text)
        else:
            print(response.text)

        print("Log into your account")
        username = raw_input("Enter username: ")
        password = raw_input("Enter password: ")
        loginPayload = {'username':username,'password':password}
        loginResponse = session.post(paymentProviderBaseUrl + "login/", data=loginPayload)
        #if log in successful
        if(loginResponse.status_code == 200):
            paymentResponse = session.post(paymentProviderBaseUrl + "payinvoice/", json=paymentPayload)
            #if not enough funds, ask to deposit money
            if(paymentResponse.status_code == 503):
                print("Insufficient funds in account.")
                print("Deposit some funds")
                accNum = raw_input("Enter account number: ")
                depositAmount = input("Enter amount: ")
                depositPayload = {'amount':depositAmount, 'account_num':accNum}
                depositResponse = session.post(paymentProviderBaseUrl + "deposit/", json=depositPayload)
                #resend payment request
                if(depositResponse.status_code == 201):
                    deposit = json.loads(depositResponse.text)
                    print("Balance has been updated.")
                    paymentResponse = session.post(paymentProviderBaseUrl + "payinvoice/", json=paymentPayload)
                    if(paymentResponse.status_code == 201):
                        payment = json.loads(paymentResponse.text)
                        finalizePayload = {'booking_num': invoice['booking_num'], 'pay_provider_id' : invoice['pay_provider_id'], 'stamp': payment['stamp_code']}
                        finalizeResponse = requests.post(BASE_URL + "finalizebooking/", json=finalizePayload)
                        if(finalizeResponse.status_code == 201):
                            #Paid for booking success
                            finalized = json.loads(finalizeResponse.text)
                            print("Booking " + finalized['booking_num'] + " is: " + finalized['booking_status'])
                        else:
                            print(finalizeResponse.text)
                    else:
                        print(paymentResponse.text)
                else:
                    print(depositResponse.text)
            else:
                print(paymentResponse.text)
            #if successful finalize with airline
            if(paymentResponse.status_code == 201):
                payment = json.loads(paymentResponse.text)
                finalizePayload = {'booking_num': invoice['booking_num'], 'pay_provider_id' : invoice['pay_provider_id'], 'stamp': payment['stamp_code']}
                finalizeResponse = requests.post(BASE_URL + "finalizebooking/", json=finalizePayload)
                if(finalizeResponse.status_code == 201):
                    #Paid for booking success
                    finalized = json.loads(finalizeResponse.text)
                    print("Booking " + finalized['booking_num'] + " is: " + finalized['booking_status'])
                else:
                    print(finalizeResponse.text)
            else:
                print(paymentResponse.text)
        else:
            print(loginResponse.text)
    else:
        print(response.text)
