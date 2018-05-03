from django.contrib import admin
from .models import Aircraft, Airport, Flight, Passenger, Booking, PaymentProvider, Invoice

class AircraftAdmin(admin.ModelAdmin):
    list_display = ('aircraft_type', 'registration_number', 'seat_capacity')
    search_fields = ('aircraft_type', 'registration_number', 'seat_capacity')

class AirportAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'time_zone')
    search_fields = ('name', 'country', 'time_zone')

class FlightAdmin(admin.ModelAdmin):
    list_display = ('flight_number', 'departure_airport', 'destination_airport', 'departure_date_time', 'arrival_date_time', 'flight_duration', 'aircraft', 'seat_price')
    search_fields = ('flight_number', 'departure_airport', 'destination_airport', 'departure_date_time', 'arrival_date_time', 'flight_duration', 'aircraft', 'seat_price')

class PassengerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'surname', 'email', 'phone_number')
    search_fields = ('first_name', 'surname', 'email', 'phone_number')

class BookingAdmin(admin.ModelAdmin):
    list_display = ('booking_number', 'flight', 'number_of_seats', 'get_passengers', 'status', 'payment_time_window')
    search_fields = ('booking_number', 'flight', 'number_of_seats', 'get_passengers', 'status', 'payment_time_window')

class PaymentProviderAdmin(admin.ModelAdmin):
    list_display = ('name', 'provider_id', 'web_address', 'account_number', 'login_username', 'login_password')
    search_fields = ('name', 'provider_id', 'web_address', 'account_number', 'login_username', 'login_password')

class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'payment_service_provider_invoice_number', 'booking_number', 'amount', 'paid', 'payment_confirmation_code')
    search_fields = ('invoice_number', 'payment_service_provider_invoice_number', 'booking_number', 'amount', 'paid', 'payment_confirmation_code')

admin.site.register(Aircraft, AircraftAdmin)
admin.site.register(Airport, AirportAdmin)
admin.site.register(Flight, FlightAdmin)
admin.site.register(Passenger, PassengerAdmin)
admin.site.register(Booking, BookingAdmin)
admin.site.register(PaymentProvider, PaymentProviderAdmin)
admin.site.register(Invoice, InvoiceAdmin)
