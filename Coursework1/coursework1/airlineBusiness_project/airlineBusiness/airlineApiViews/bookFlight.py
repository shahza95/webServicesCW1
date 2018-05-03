from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from airline.models import *
from random import randint
import json
import datetime

#TESTING VIA TERMINAL
# python shell
# import requests
# import json
# payload = {'flight_id': 'JY2369', 'passengers': [{'first_name' : 'Shahza', 'surname': 'Syed', 'email': 'll13s6s@leeds.ac.uk', 'phone_number': '07268330276'},{'first_name' : 'John', 'surname': 'Smith', 'email': 'test@leeds.ac.uk', 'phone_number': '07668754276'}]}
# url = 'http://127.0.0.1:8000/api/bookflight/'
# r = requests.post(url, json=payload)

# find a flight- parameters:  departure date, departure airport, destination airport, date_flex (true (1 day)/false)
@csrf_exempt
def bookFlight(request):
    has_error = False
    error_message = 'Error:\n'
    json_data = {}
    flightId = ""
    passengers = []

    if(request.method != 'POST'):
        has_error = True
        error_message += 'Only POST requests allowed for this resource\n'

    headers = request.META
    content_type = headers['CONTENT_TYPE']
    if content_type != 'application/json':
        has_error = True
        error_message += 'Payload must be a json object\n'

    try:
        payload = request.body
        json_data = json.loads(payload)
    except ValueError:
        has_error = True
        error_message += 'invalid json object\n'

    try:
        flightId = str(json_data['flight_id'])
        passengers = json_data['passengers']

    except KeyError:
        has_error = True
        error_message += 'expected json key not found in payload\n'


#####   CHECK SEATS AVAILABLE? - currently no mechanism to fail a request for booking
    bookingPassengers = []

    #Retrieve flight
    flight = Flight.objects.get(flight_number = flightId)
    #Create booking
    booking = Booking.objects.create(booking_number = generateRandomBookingNumber(), flight = flight, number_of_seats = len(passengers), payment_time_window = datetime.timedelta(minutes=10))
    #Add passengers & associate to booking
    for passenger in passengers:
        booking.passenger_details.create(first_name = passenger['first_name'], surname = passenger['surname'], email = passenger['email'], phone_number = passenger['phone'])

    #Return booking details in payload - number, status and total price
    #Calculate total price
    pricePerSeat = flight.seat_price
    totalPrice = pricePerSeat * len(passengers)
    payload = {'booking_num': booking.booking_number, 'booking_status' : booking.status, 'tot_price' : totalPrice}

    if (has_error):
        http_response = HttpResponseBadRequest ()
        http_response['Content-Type'] = 'text/plain'
        http_response.content = error_message
        http_response.status_code = 503
        http_response.reason_phrase = 'Service Unavailable'
        return http_response

    http_response = HttpResponse (json.dumps(payload))
    http_response['Content-Type'] = 'application/json'
    http_response.status_code = 201
    http_response.reason_phrase = 'CREATED'
    return http_response

#Helper method to geenerate a booking number
def generateRandomBookingNumber():
    return ''.join(["%s" % randint(0, 9) for num in range(0, 10)])
