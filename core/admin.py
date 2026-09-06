from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, City, Theatre, Screen, Seat, Movie, Show, Booking

admin.site.register(User, UserAdmin)
admin.site.register(City)
admin.site.register(Theatre)
admin.site.register(Screen)
admin.site.register(Seat)
admin.site.register(Movie)
admin.site.register(Show)
admin.site.register(Booking)
