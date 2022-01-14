from django.contrib import admin

from main.models import Airplane, Country, Ticket, Person

admin.site.register(Airplane)
admin.site.register(Country)
admin.site.register(Person)
admin.site.register(Ticket)
