from django.core.management.base import BaseCommand
from core.models import City, Theatre, Screen, Seat, Movie, Show
from datetime import datetime, timedelta
from django.utils.timezone import make_aware

class Command(BaseCommand):
    help = 'Seed the database with sample MovieBook data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Deleting old data...')
        Show.objects.all().delete()
        Seat.objects.all().delete()
        Screen.objects.all().delete()
        Theatre.objects.all().delete()
        City.objects.all().delete()
        Movie.objects.all().delete()

        self.stdout.write('Creating Cities...')
        cities_data = ['Pune', 'Pimpri-Chinchwad', 'Mumbai', 'Nashik', 'Nagpur', 'Thane', 'Bengaluru', 'Hyderabad', 'Delhi', 'Chennai']
        cities = {}
        for c in cities_data:
            cities[c] = City.objects.create(name=c)

        self.stdout.write('Creating Theatres & Screens...')
        theatres_data = [
            {'name': 'PVR Cinemas', 'address': 'Phoenix Mall, Viman Nagar', 'city': 'Pune', 'distance': 3.2, 'rating': 4.4},
            {'name': 'INOX', 'address': 'Bund Garden Road', 'city': 'Pune', 'distance': 5.7, 'rating': 4.2},
            {'name': 'Cinepolis', 'address': 'Seasons Mall, Magarpatta', 'city': 'Pune', 'distance': 4.1, 'rating': 4.5},
            {'name': 'City Pride', 'address': 'Kothrud', 'city': 'Pune', 'distance': 2.5, 'rating': 4.0},
            {'name': 'PVR Cinemas', 'address': 'Elpro City Square', 'city': 'Pimpri-Chinchwad', 'distance': 2.1, 'rating': 4.3},
            {'name': 'INOX', 'address': 'Jai Ganesh Vision', 'city': 'Pimpri-Chinchwad', 'distance': 3.4, 'rating': 4.1},
        ]
        
        theatres = []
        for td in theatres_data:
            t = Theatre.objects.create(
                name=td['name'], address=td['address'], city=cities[td['city']], 
                distance=td['distance'], rating=td['rating']
            )
            theatres.append(t)
            # Create screens and seats for each theatre
            for s_idx in range(1, 4):
                screen = Screen.objects.create(name=f"Screen {s_idx}", theatre=t)
                # Create standard seats
                for row in ['A', 'B', 'C', 'D', 'E']:
                    for num in range(1, 11):
                        Seat.objects.create(
                            number=f"{row}{num}", seat_type='STANDARD', 
                            price=180.00, screen=screen
                        )
                # Create premium seats
                for row in ['F', 'G']:
                    for num in range(1, 11):
                        Seat.objects.create(
                            number=f"{row}{num}", seat_type='PREMIUM', 
                            price=300.00, screen=screen
                        )

        self.stdout.write('Creating Movies...')
        movies_data = [
            {
                'title': 'Dune: Part Two', 'genre': 'Sci-Fi/Action', 'language': 'English', 'duration': 166,
                'rating': 4.8, 'certificate': 'U/A', 'release_date': '2024-03-01',
                'description': 'Paul Atreides unites with Chani and the Fremen while on a warpath of revenge against the conspirators who destroyed his family.',
                'cast': 'Timothée Chalamet, Zendaya, Rebecca Ferguson', 'director': 'Denis Villeneuve',
                'poster_url': 'https://image.tmdb.org/t/p/w500/1pdfLvkbY9ohJlCjQH2JGqq995O.jpg',
                'banner_url': 'https://image.tmdb.org/t/p/original/8rpDcsfLJypbO6vtecsmEZzAUoa.jpg',
                'trailer_url': 'https://www.youtube.com/watch?v=Way9Dexny3w'
            },
            {
                'title': 'Fighter', 'genre': 'Action/Thriller', 'language': 'Hindi', 'duration': 166,
                'rating': 4.2, 'certificate': 'U/A', 'release_date': '2024-01-25',
                'description': 'Top IAF aviators come together in the face of imminent danger, to form Air Dragons.',
                'cast': 'Hrithik Roshan, Deepika Padukone, Anil Kapoor', 'director': 'Siddharth Anand',
                'poster_url': 'https://image.tmdb.org/t/p/w500/zEqyD0SBt6HL7GlNdUaIE6BpwYc.jpg',
                'banner_url': 'https://image.tmdb.org/t/p/original/aINel9503dp0gI2o1Ata9Zqf9Z7.jpg',
                'trailer_url': 'https://www.youtube.com/watch?v=6amIq_mP4xM'
            },
            {
                'title': 'Kalki 2898 AD', 'genre': 'Sci-Fi/Action', 'language': 'Telugu', 'duration': 180,
                'rating': 4.5, 'certificate': 'U/A', 'release_date': '2024-05-09',
                'description': 'A modern-day avatar of Vishnu, a Hindu god, who is believed to have descended to earth to protect the world from evil forces.',
                'cast': 'Prabhas, Deepika Padukone, Amitabh Bachchan', 'director': 'Nag Ashwin',
                'poster_url': 'https://image.tmdb.org/t/p/w500/xZN4i2Y8lWv08G2PzWwUjFfR92.jpg',
                'banner_url': 'https://image.tmdb.org/t/p/original/3mKz8qf5o4rO5v3F8uO1VjQ3Q8A.jpg',
                'trailer_url': 'https://www.youtube.com/watch?v=kQ9P9aX2o1U'
            },
            {
                'title': 'Kung Fu Panda 4', 'genre': 'Animation/Comedy', 'language': 'English', 'duration': 94,
                'rating': 4.1, 'certificate': 'U', 'release_date': '2024-03-08',
                'description': 'After Po is tapped to become the Spiritual Leader of the Valley of Peace, he needs to find and train a new Dragon Warrior.',
                'cast': 'Jack Black, Awkwafina, Viola Davis', 'director': 'Mike Mitchell',
                'poster_url': 'https://image.tmdb.org/t/p/w500/kDp1vUBnMpe8ak4rjgl3cLELqjU.jpg',
                'banner_url': 'https://image.tmdb.org/t/p/original/1XDDXPXGi18c1OdEQZTXFqsrOn.jpg',
                'trailer_url': 'https://www.youtube.com/watch?v=_inKs4eeHiI'
            },
            {
                'title': 'Maharashtra Shahir', 'genre': 'Biography/Drama', 'language': 'Marathi', 'duration': 150,
                'rating': 4.6, 'certificate': 'U', 'release_date': '2023-04-28',
                'description': 'Biopic of Shahir Sable, a leading folk singer and artist from Maharashtra.',
                'cast': 'Ankush Chaudhari, Sana Shinde', 'director': 'Kedar Shinde',
                'poster_url': 'https://image.tmdb.org/t/p/w500/6oK1a78oZc8b1z3j4j5f6X9o7T8.jpg',
                'banner_url': 'https://image.tmdb.org/t/p/original/1T2z9x2Y7Z6x2b5q1w8e3r4T1o3.jpg',
                'trailer_url': 'https://www.youtube.com/watch?v=3r1q5o1T2z9'
            },
            {
                'title': 'Godzilla x Kong: The New Empire', 'genre': 'Action/Sci-Fi', 'language': 'English', 'duration': 115,
                'rating': 4.0, 'certificate': 'U/A', 'release_date': '2024-03-29',
                'description': 'Two ancient titans, Godzilla and Kong, clash in an epic battle as humans unravel their intertwined origins.',
                'cast': 'Rebecca Hall, Brian Tyree Henry', 'director': 'Adam Wingard',
                'poster_url': 'https://image.tmdb.org/t/p/w500/tMefBSflR6PGQLvLuPEIQfUF12j.jpg',
                'banner_url': 'https://image.tmdb.org/t/p/original/sR0SpCrXamlIkYMdfz83sFn5JS6.jpg',
                'trailer_url': 'https://www.youtube.com/watch?v=lV1OOlGwExM'
            },
            {
                'title': 'Pushpa 2: The Rule', 'genre': 'Action/Drama', 'language': 'Telugu', 'duration': 175,
                'rating': 4.7, 'certificate': 'A', 'release_date': '2024-08-15',
                'description': 'The clash between Pushpa Raj and SP Bhanwar Singh Shekhawat continues in this epic sequel.',
                'cast': 'Allu Arjun, Fahadh Faasil, Rashmika Mandanna', 'director': 'Sukumar',
                'poster_url': 'https://image.tmdb.org/t/p/w500/1pdfLvkbY9ohJlCjQH2JGqq995O.jpg',
                'banner_url': 'https://image.tmdb.org/t/p/original/1pdfLvkbY9ohJlCjQH2JGqq995O.jpg',
                'trailer_url': 'https://www.youtube.com/watch?v=Q1NKMPhP8PI'
            },
            {
                'title': 'Crew', 'genre': 'Comedy', 'language': 'Hindi', 'duration': 120,
                'rating': 4.3, 'certificate': 'U/A', 'release_date': '2024-03-29',
                'description': 'Three hard-working women find themselves caught in a web of lies and unexpected situations.',
                'cast': 'Tabu, Kareena Kapoor, Kriti Sanon', 'director': 'Rajesh Krishnan',
                'poster_url': 'https://image.tmdb.org/t/p/w500/8r1q5o1T2z9x2b5q1w8e3r4T1o3.jpg',
                'banner_url': 'https://image.tmdb.org/t/p/original/8r1q5o1T2z9x2b5q1w8e3r4T1o3.jpg',
                'trailer_url': 'https://www.youtube.com/watch?v=8r1q5o1T2z9'
            },
            {
                'title': 'Bramayugam', 'genre': 'Horror/Thriller', 'language': 'Malayalam', 'duration': 140,
                'rating': 4.8, 'certificate': 'U/A', 'release_date': '2024-02-15',
                'description': 'A young singer strays into a mysterious manor, setting off a chain of supernatural events.',
                'cast': 'Mammootty, Arjun Ashokan', 'director': 'Rahul Sadasivan',
                'poster_url': 'https://image.tmdb.org/t/p/w500/1pdfLvkbY9ohJlCjQH2JGqq995O.jpg',
                'banner_url': 'https://image.tmdb.org/t/p/original/1pdfLvkbY9ohJlCjQH2JGqq995O.jpg',
                'trailer_url': 'https://www.youtube.com/watch?v=1pdfLvkbY9oh'
            },
            {
                'title': 'Inside Out 2', 'genre': 'Animation/Comedy', 'language': 'English', 'duration': 100,
                'rating': 4.6, 'certificate': 'U', 'release_date': '2024-06-14',
                'description': 'Follow Riley into her teenage years, introducing new emotions to the headquarters.',
                'cast': 'Amy Poehler, Phyllis Smith, Lewis Black', 'director': 'Kelsey Mann',
                'poster_url': 'https://image.tmdb.org/t/p/w500/xZN4i2Y8lWv08G2PzWwUjFfR92.jpg',
                'banner_url': 'https://image.tmdb.org/t/p/original/xZN4i2Y8lWv08G2PzWwUjFfR92.jpg',
                'trailer_url': 'https://www.youtube.com/watch?v=xZN4i2Y8lWv'
            }
        ]

        movies = []
        for md in movies_data:
            m = Movie.objects.create(
                title=md['title'], genre=md['genre'], language=md['language'],
                duration=md['duration'], rating=md['rating'], certificate=md['certificate'],
                release_date=datetime.strptime(md['release_date'], '%Y-%m-%d').date(),
                description=md['description'], cast=md['cast'], director=md['director'],
                poster_url=md['poster_url'], banner_url=md['banner_url'], trailer_url=md['trailer_url']
            )
            movies.append(m)

        self.stdout.write('Creating Shows...')
        # Create shows for the next 3 days
        now = datetime.now()
        for i in range(3):
            show_date = now + timedelta(days=i)
            for theatre in theatres:
                for screen in theatre.screens.all():
                    # Pick a random movie
                    import random
                    movie = random.choice(movies)
                    # Create 4 showtimes
                    times = [10, 13, 16, 20] # 10am, 1pm, 4pm, 8pm
                    for h in times:
                        st = show_date.replace(hour=h, minute=0, second=0, microsecond=0)
                        Show.objects.create(
                            movie=movie, screen=screen, start_time=make_aware(st)
                        )

        self.stdout.write(self.style.SUCCESS('Successfully seeded database!'))
