from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('movie/<int:movie_id>/', views.movie_details, name='movie_details'),
    path('city/<str:city_name>/', views.set_city, name='set_city'),
    path('book/<int:show_id>/', views.seat_selection, name='seat_selection'),
    path('checkout/<int:show_id>/', views.checkout, name='checkout'),
    path('ticket/<str:booking_id>/', views.ticket, name='ticket'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('custom-admin/', views.admin_dashboard, name='custom_admin'),
]
