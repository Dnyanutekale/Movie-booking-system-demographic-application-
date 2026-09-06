from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # Django provides id, username, email, password out of the box
    is_admin = models.BooleanField(default=False)

class City(models.Model):
    name = models.CharField(max_length=100, unique=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Cities"

class Theatre(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField()
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='theatres')
    distance = models.FloatField(help_text="Mock distance for MVP")
    rating = models.FloatField(default=0.0)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.name} - {self.city.name}"

class Screen(models.Model):
    name = models.CharField(max_length=100)
    theatre = models.ForeignKey(Theatre, on_delete=models.CASCADE, related_name='screens')
    
    def __str__(self):
        return f"{self.name} ({self.theatre.name})"

class Seat(models.Model):
    SEAT_TYPES = (('STANDARD', 'Standard'), ('PREMIUM', 'Premium'), ('RECLINER', 'Recliner'))
    number = models.CharField(max_length=10)
    seat_type = models.CharField(max_length=20, choices=SEAT_TYPES)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    screen = models.ForeignKey(Screen, on_delete=models.CASCADE, related_name='seats')
    
    def __str__(self):
        return f"{self.number} ({self.seat_type}) - {self.screen.name}"

class Movie(models.Model):
    title = models.CharField(max_length=255)
    poster_url = models.URLField(max_length=500)
    banner_url = models.URLField(max_length=500)
    genre = models.CharField(max_length=100)
    language = models.CharField(max_length=100)
    duration = models.IntegerField(help_text="Duration in minutes")
    rating = models.FloatField()
    certificate = models.CharField(max_length=10)
    release_date = models.DateField()
    description = models.TextField()
    cast = models.TextField()
    director = models.CharField(max_length=255)
    trailer_url = models.URLField(max_length=500)
    
    def __str__(self):
        return self.title

class Show(models.Model):
    FORMAT_CHOICES = (('2D', '2D'), ('3D', '3D'), ('IMAX', 'IMAX 3D'), ('4DX', '4DX'))
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='shows')
    screen = models.ForeignKey(Screen, on_delete=models.CASCADE, related_name='shows')
    start_time = models.DateTimeField()
    format = models.CharField(max_length=10, choices=FORMAT_CHOICES, default='2D')
    language = models.CharField(max_length=50, default='Hindi')
    
    def __str__(self):
        return f"{self.movie.title} - {self.screen.theatre.name} - {self.start_time.strftime('%Y-%m-%d %H:%M')}"

class Booking(models.Model):
    STATUS_CHOICES = (('PENDING', 'Pending'), ('SUCCESS', 'Success'), ('FAILED', 'Failed'), ('CANCELLED', 'Cancelled'))
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    show = models.ForeignKey(Show, on_delete=models.CASCADE, related_name='bookings')
    seats = models.JSONField(help_text="List of seat IDs or numbers")
    ticket_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    convenience_fee = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)
    taxes = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    booking_id = models.CharField(max_length=50, unique=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Booking {self.booking_id} - {self.user.username}"
