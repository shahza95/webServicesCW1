from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from airline.models import *
from random import randint
import requests
import json
import datetime

#TESTING VIA TERMINAL- view all
# python shell
# import requests
# import json
# payload={'company_type':'payment'}
# url= 'http://directory.pythonanywhere.com/api/list/'
# r = requests.get(url, json=payload)

# get and display all possible payment methods (providers)

PAYMENT_PROVIDER_OF_BUSINESS = "Iron Bank"

@csrf_exempt
def paymentMethods(request):
    has_error = False
    error_message = 'Error:\n'
    returnPayload = {}

    if(request.method != 'GET'):
        has_error = True
        error_message += 'Only GET requests allowed for this resource\n'

    headers = request.META
    content_type = headers['CONTENT_TYPE']
    if content_type != 'application/json':
        has_error = True
        error_message += 'Payload must be a json object\n'

    #get all payment providers and return in a list
    providers_list = PaymentProvider.objects.all()
    if not providers_list:
        http_response = HttpResponse ("No possible payment providers available")
        http_response['Content-Type'] = 'text/plain'
        http_response.status_code = 503
        http_response.reason_phrase = 'Service Unavailable'
        return http_response

    providers = []
    for record in providers_list:
        item = {'pay_provider_id' : record.provider_id, 'pay_provider_name' : record.name}
        providers.append(item)

    returnPayload = {'providers' : providers}

    if (has_error):
        http_response = HttpResponseBadRequest ()
        http_response['Content-Type'] = 'text/plain'
        http_response.content = error_message
        http_response.status_code = 503
        http_response.reason_phrase = 'Service Unavailable'
        return http_response

    http_response = HttpResponse (json.dumps(returnPayload))
    http_response['Content-Type'] = 'application/json'
    http_response.status_code = 200
    http_response.reason_phrase = 'OK'
    return http_response
