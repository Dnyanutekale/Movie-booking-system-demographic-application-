from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Movie, City, Theatre, Show, Booking, Seat
import json
import uuid

def home(request):
    current_city_name = request.session.get('city', 'Pune')
    try:
        current_city = City.objects.get(name=current_city_name)
    except City.DoesNotExist:
        current_city = City.objects.first()
        current_city_name = current_city.name if current_city else None
        
    cities = City.objects.all()
    
    # Get movies playing in this city
    shows_in_city = Show.objects.filter(
        screen__theatre__city=current_city,
        start_time__gte=timezone.now()
    ).select_related('movie')
    
    movie_ids = shows_in_city.values_list('movie_id', flat=True).distinct()
    now_showing_qs = Movie.objects.filter(id__in=movie_ids)
    now_showing = list(now_showing_qs[:5])
    
    # Upcoming or all other movies
    upcoming = Movie.objects.exclude(id__in=movie_ids)[:5]
    
    # Theatres in city
    theatres = Theatre.objects.filter(city=current_city).order_by('distance')[:4]
    
    context = {
        'cities': cities,
        'current_city': current_city_name,
        'now_showing': now_showing,
        'upcoming': upcoming,
        'theatres': theatres,
        'featured': now_showing[0] if now_showing else None,
    }
    return render(request, 'core/home.html', context)

def set_city(request, city_name):
    request.session['city'] = city_name
    return redirect('home')

def movie_details(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    current_city_name = request.session.get('city', 'Pune')
    cities = City.objects.all()
    
    # Get showtimes for this movie in the current city
    shows = Show.objects.filter(
        movie=movie,
        screen__theatre__city__name=current_city_name,
        start_time__gte=timezone.now()
    ).order_by('screen__theatre', 'start_time')
    
    # Group shows by theatre
    theatre_shows = {}
    for show in shows:
        t = show.screen.theatre
        if t not in theatre_shows:
            theatre_shows[t] = []
        theatre_shows[t].append(show)
        
    context = {
        'movie': movie,
        'current_city': current_city_name,
        'cities': cities,
        'theatre_shows': theatre_shows,
    }
    return render(request, 'core/movie_details.html', context)

def seat_selection(request, show_id):
    show = get_object_or_404(Show, id=show_id)
    screen = show.screen
    seats = Seat.objects.filter(screen=screen)
    
    # Find booked seats
    bookings = Booking.objects.filter(show=show, payment_status='SUCCESS')
    booked_seat_ids = []
    for b in bookings:
        booked_seat_ids.extend(json.loads(b.seats))
        
    context = {
        'show': show,
        'seats': seats,
        'booked_seat_ids': json.dumps(booked_seat_ids),
        'premium_price': 300,
        'standard_price': 180,
    }
    return render(request, 'core/seat_selection.html', context)

def checkout(request, show_id):
    if request.method != 'POST':
        return redirect('seat_selection', show_id=show_id)
        
    show = get_object_or_404(Show, id=show_id)
    selected_seats = json.loads(request.POST.get('selected_seats', '[]'))
    
    if not selected_seats:
        return redirect('seat_selection', show_id=show_id)
        
    seats = Seat.objects.filter(id__in=selected_seats)
    total_price = sum(seat.price for seat in seats)
    convenience_fee = len(selected_seats) * 30
    taxes = float(total_price) * 0.18
    total_amount = float(total_price) + convenience_fee + taxes
    
    if request.POST.get('action') == 'pay':
        # Process mock payment
        booking = Booking.objects.create(
            user=request.user if request.user.is_authenticated else User.objects.first(),
            show=show,
            seats=json.dumps(selected_seats),
            ticket_price=total_price,
            convenience_fee=convenience_fee,
            taxes=taxes,
            total_amount=total_amount,
            payment_status='SUCCESS',
            booking_id=str(uuid.uuid4().hex)[:10].upper()
        )
        return redirect('ticket', booking_id=booking.booking_id)
        
    context = {
        'show': show,
        'selected_seats': seats,
        'total_price': total_price,
        'convenience_fee': convenience_fee,
        'taxes': round(taxes, 2),
        'total_amount': round(total_amount, 2),
        'selected_seats_json': request.POST.get('selected_seats'),
    }
    return render(request, 'core/checkout.html', context)

def ticket(request, booking_id):
    booking = get_object_or_404(Booking, booking_id=booking_id)
    seats = Seat.objects.filter(id__in=json.loads(booking.seats))
    seat_numbers = [s.number for s in seats]
    
    context = {
        'booking': booking,
        'seat_numbers': ", ".join(seat_numbers),
    }
    return render(request, 'core/ticket.html', context)

def my_bookings(request):
    user = request.user if request.user.is_authenticated else User.objects.first()
    bookings = Booking.objects.filter(user=user, payment_status='SUCCESS').order_by('-created_at')
    
    upcoming = []
    past = []
    now = timezone.now()
    
    for b in bookings:
        if b.show.start_time > now:
            upcoming.append(b)
        else:
            past.append(b)
            
    for b in upcoming + past:
        seat_ids = json.loads(b.seats)
        b.seat_names = ", ".join(Seat.objects.filter(id__in=seat_ids).values_list('number', flat=True))
        
    context = {
        'upcoming': upcoming,
        'past': past,
        'cities': City.objects.all(),
        'current_city': request.session.get('city', 'Pune')
    }
    return render(request, 'core/my_bookings.html', context)

from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def admin_dashboard(request):
    today = timezone.now().date()
    context = {
        'total_users': User.objects.count(),
        'total_movies': Movie.objects.count(),
        'total_cinemas': Theatre.objects.count(),
        'today_bookings': Booking.objects.filter(created_at__date=today).count(),
        'recent_bookings': Booking.objects.order_by('-created_at')[:5],
    }
    return render(request, 'core/admin_dashboard.html', context)
