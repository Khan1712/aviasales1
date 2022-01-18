from django.contrib import admin

from main.models import Airplane, Country, Ticket, Person, Comment, Likes, Rating

admin.site.register(Airplane)
admin.site.register(Country)
admin.site.register(Person)
admin.site.register(Ticket)
admin.site.register(Comment)
admin.site.register(Likes)
admin.site.register(Rating)
