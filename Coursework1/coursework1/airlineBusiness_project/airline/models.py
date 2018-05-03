from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
import uuid

class Aircraft(models.Model):
    aircraft_type = models.CharField(max_length=30)
    registration_number = models.CharField(max_length=30)
    seat_capacity = models.PositiveIntegerField()

    def __str__(self):
        return self.aircraft_type

class Airport(models.Model):
    name = models.CharField(max_length=30)
    country = models.CharField(max_length=30)
    time_zone = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Flight(models.Model):
    flight_number = models.CharField(max_length=10)
    departure_airport = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name='departure_airport')
    destination_airport = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name='arrival_airport')
    departure_date_time = models.DateTimeField()
    arrival_date_time = models.DateTimeField()
    flight_duration = models.DurationField()
    aircraft = models.ForeignKey(Aircraft, on_delete=models.CASCADE)
    seat_price = models.FloatField()

    def __str__(self):
        return self.flight_number

class Passenger(models.Model):
    first_name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    email = models.EmailField()
    phone_number = PhoneNumberField()

    def __str__(self):
        return u'%s %s' % (self.first_name, self.surname)

class Booking(models.Model):
    booking_number = models.CharField(max_length=10)
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    number_of_seats = models.PositiveIntegerField()
    passenger_details = models.ManyToManyField(Passenger)
    STATUS_CHOICES = (
        ('OnHold', 'On hold'),
        ('Confirmed', 'Confirmed'),
        ('Cancelled', 'Cancelled'),
        ('Travelled', 'Travelled'),
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='OnHold',)
    payment_time_window = models.DurationField()

    def __str__(self):
        return self.booking_number

    def get_passengers(self):
        return "\n".join([p.first_name for p in self.passenger_details.all()])

class PaymentProvider(models.Model):
    name = models.CharField(max_length=30)
    provider_id = models.CharField(max_length=10)
    web_address = models.URLField()
    account_number = models.PositiveIntegerField()
    login_username = models.CharField(max_length=30)
    login_password = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Invoice(models.Model):
    invoice_number = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    payment_service_provider_invoice_number = models.CharField(max_length=30)
    booking_number = models.ForeignKey(Booking, on_delete=models.CASCADE)
    amount = models.FloatField()
    paid = models.BooleanField()
    payment_confirmation_code = models.CharField(max_length=10)

    def __str__(self):
        return self.invoice_number
