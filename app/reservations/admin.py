from django.contrib import admin

# Register your models here.
from reservations.models import *

admin.site.register(Movie)
admin.site.register(Theater)
admin.site.register(Reservation)
admin.site.register(Auditorium)
admin.site.register(Seat)
admin.site.register(Screening)