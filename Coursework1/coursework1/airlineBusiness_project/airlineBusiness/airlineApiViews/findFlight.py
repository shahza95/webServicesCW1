from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from airline.models import *
import json
import datetime

DATE_FLEX_PERIOD = 3

#TESTING VIA TERMINAL
# python shell
# import requests
# import json
# payload = {'dep_airport': 'London', 'dest_airport': 'Manchester', 'dep_date':'2018-04-30', 'num_passengers':1, 'is_flex':False}
# url = 'http://127.0.0.1:8000/api/findflight/'
# r = requests.get(url, json=payload)

# find a flight- parameters:  departure date, departure airport, destination airport, date_flex (true (1 day)/false)
@csrf_exempt
def findFlight(request):
    has_error = False
    error_message = 'Error:\n'
    json_data = {}
    isFlex = False
    departureAirport = ""
    destinationAirport = ""
    departureDate = ""

    if(request.method != 'GET'):
        has_error = True
        error_message += 'Only GET requests allowed for this resource\n'

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
        departureAirport = str(json_data['dep_airport'])
        destinationAirport = json_data['dest_airport']
        departureDate = json_data['dep_date']
        numberOfPassengers = json_data['num_passengers']
        isFlex = json_data['is_flex']
    except KeyError:
        has_error = True
        error_message += 'expected json key not found in payload\n'

    #date must be in form yyyy-mm-dd
    if isFlex:
        print(getDateFlexRange2(departureDate))
        flights_list = Flight.objects.filter(departure_airport__name__contains = departureAirport,
            destination_airport__name__contains = destinationAirport, departure_date_time__range = [getDateFlexRange1(departureDate), getDateFlexRange2(departureDate)])
    else:
        flights_list = Flight.objects.filter(departure_airport__name__contains = departureAirport,
            destination_airport__name__contains = destinationAirport, departure_date_time__date = departureDate)

    if not flights_list:
        http_response = HttpResponse ("No flights found.")
        http_response['Content-Type'] = 'text/plain'
        http_response.status_code = 503
        http_response.reason_phrase = 'Service Unavailable'
        return http_response

    flights = []
    for record in flights_list:
        item ={'flight_id': record.id, 'flight_num': record.flight_number, 'dep_airport': str(record.departure_airport), 'dest_airport': str(record.destination_airport), 'dep_datetime': record.departure_date_time, 'arr_datetime': record.arrival_date_time, 'duration': record.flight_duration, 'price': record.seat_price}
        flights.append(item)
    payload = {'flights': flights}

    if (has_error):
        http_response = HttpResponseBadRequest ()
        http_response['Content-Type'] = 'text/plain'
        http_response.content = error_message
        return http_response

    http_response = HttpResponse (json.dumps(payload, default=dateTimeConverter))
    http_response['Content-Type'] = 'application/json'
    http_response.status_code = 200
    http_response.reason_phrase = 'OK'
    return http_response


#helper method to return flex date range format: ["yyyy-mm-dd", "yyyy-mm-dd"]
def getDateFlexRange1(departureDate):
    year, month, day = departureDate.split("-")
    return year + '-' + month + '-' + str(int(day) - DATE_FLEX_PERIOD)

def getDateFlexRange2(departureDate):
    year, month, day = departureDate.split("-")
    return year + '-' + month + '-' + str(int(day) + DATE_FLEX_PERIOD)

def dateTimeConverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()
