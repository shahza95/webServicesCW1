from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from airline.models import *
import json
import datetime

@csrf_exempt
def bookingStatus(request):
    has_error = False
    error_message = 'Error:\n'
    json_data = {}
    booking_num = ""

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
        booking_num = str(json_data['booking_num'])
    except KeyError:
        has_error = True
        error_message += 'expected json key not found in payload\n'


    #Retrieve booking
    booking = Booking.objects.get(booking_number = booking_num)
    #formulate return payload
    payload = {'booking_num':booking.booking_number, 'booking_status' : booking.status, 'flight_num':booking.flight.flight_number, 'dep_airport':booking.flight.departure_airport.name, 'dest_airport':booking.flight.destination_airport.name, 'dep_datetime': booking.flight.departure_date_time, 'arr_datetime': booking.flight.arrival_date_time, 'duration':str(booking.flight.flight_duration)}

    if (has_error):
        http_response = HttpResponseBadRequest ()
        http_response['Content-Type'] = 'text/plain'
        http_response.content = error_message
        http_response.status_code = 503
        http_response.reason_phrase = 'Service Unavailable'
        return http_response

    http_response = HttpResponse (json.dumps(payload, default=dateTimeConverter))
    http_response['Content-Type'] = 'application/json'
    http_response.status_code = 200
    http_response.reason_phrase = 'OK'
    return http_response

#helper method for serializing timedelta values
def dateTimeConverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()
