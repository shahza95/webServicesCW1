from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from airline.models import *
import json
import datetime

@csrf_exempt
def cancelBooking(request):
    has_error = False
    error_message = 'Error:\n'
    json_data = {}
    booking_num = ""

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
        booking_num = str(json_data['booking_num'])
    except KeyError:
        has_error = True
        error_message += 'expected json key not found in payload\n'


    #Retrieve booking
    booking = Booking.objects.get(booking_number = booking_num)
    #cancel status & save
    booking.status = "Cancelled"
    booking.save()
    #formulate return payload
    payload = {'booking_num':booking.booking_number, 'booking_status' : booking.status}

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
