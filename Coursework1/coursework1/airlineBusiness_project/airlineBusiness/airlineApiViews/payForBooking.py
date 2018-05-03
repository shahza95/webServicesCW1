from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from airline.models import *
from random import randint
from requests import Session
import json
import datetime

@csrf_exempt
def payForBooking(request):
    has_error = False
    error_message = 'Error:\n'
    json_data = {}
    invoice = {}
    returnPayload = {}

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
        #log in as business into payment provider
        #retrieve payment provider & details
        provider = PaymentProvider.objects.get(provider_id = json_data['pay_provider_id'])
        base_url = provider.web_address
        payload = {'username':provider.login_username, 'password':provider.login_password}
        session = Session()
        r = session.post(base_url + "login/", data=payload)
        #GET COST OF BOOKING!
        # retrieve booking
        booking = Booking.objects.get(booking_number = json_data['booking_num'])
        # get number of passengers
        numPassengers = booking.number_of_seats
        # retrieve flight
        # get price
        price = booking.flight.seat_price
        # cost = numPassengers x price
        totalCost = numPassengers * price

        payload = {'account_num' : str(provider.account_number), 'client_ref_num' : json_data['booking_num'], 'amount':totalCost}
        response = session.post(base_url + "createinvoice/", json=payload)
        print("just created invoice at provider")
        if(response.status_code == 201):
            invoice = json.loads(response.text)
            #Store the invoice
            Invoice.objects.create(payment_service_provider_invoice_number = invoice['payprovider_ref_num'], booking_number = booking, amount = totalCost, paid = False, payment_confirmation_code = invoice['stamp_code'])
            print("Invoice has been generated")
            returnPayload = {'pay_provider_id': json_data['pay_provider_id'], 'invoice_id' : invoice['payprovider_ref_num'], 'booking_num' : json_data['booking_num'], 'url': provider.web_address, 'amount':totalCost}
        else:
            error_message = 'Could not create invoice'
    except KeyError:
        has_error = True
        error_message += 'expected json key not found in payload\n'

    if (has_error):
        http_response = HttpResponseBadRequest ()
        http_response['Content-Type'] = 'text/plain'
        http_response.content = error_message
        http_response.status_code = 503
        http_response.reason_phrase = 'Service Unavailable'
        return http_response

    http_response = HttpResponse (json.dumps(returnPayload))
    http_response['Content-Type'] = 'application/json'
    http_response.status_code = 201
    http_response.reason_phrase = 'CREATED'
    return http_response
