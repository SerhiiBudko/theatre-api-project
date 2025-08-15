from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from tickets.models import TheatreHall, Genre, Actor, Play, Performance


class Command(BaseCommand):
    help = 'Create sample data for theatre API'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')

        hall1, created = TheatreHall.objects.get_or_create(
            name="Main Hall",
            defaults={'rows': 20, 'seats_in_row': 25}
        )
        if created:
            self.stdout.write(f'Created theatre hall: {hall1}')

        hall2, created = TheatreHall.objects.get_or_create(
            name="Small Hall",
            defaults={'rows': 10, 'seats_in_row': 15}
        )
        if created:
            self.stdout.write(f'Created theatre hall: {hall2}')

        genres_data = [
            "Drama", "Comedy", "Tragedy", "Musical", "Thriller"
        ]
        genres = []
        for genre_name in genres_data:
            genre, created = Genre.objects.get_or_create(name=genre_name)
            if created:
                self.stdout.write(f'Created genre: {genre}')
            genres.append(genre)

        actors_data = [
            ("John", "Doe"),
            ("Jane", "Smith"),
            ("Mike", "Johnson"),
            ("Sarah", "Wilson"),
            ("David", "Brown")
        ]
        actors = []
        for first_name, last_name in actors_data:
            actor, created = Actor.objects.get_or_create(
                first_name=first_name,
                last_name=last_name
            )
            if created:
                self.stdout.write(f'Created actor: {actor}')
            actors.append(actor)

        plays_data = [
            {
                "title": "Hamlet",
                "description": "The tragedy of the Prince of Denmark",
                "genres": ["Drama", "Tragedy"],
                "actors": ["John Doe", "Jane Smith"]
            },
            {
                "title": "Romeo and Juliet",
                "description": "A tragic love story",
                "genres": ["Drama", "Tragedy"],
                "actors": ["Mike Johnson", "Sarah Wilson"]
            },
            {
                "title": "The Comedy of Errors",
                "description": "A hilarious comedy of mistaken identities",
                "genres": ["Comedy"],
                "actors": ["David Brown", "Jane Smith"]
            }
        ]

        for play_data in plays_data:
            play, created = Play.objects.get_or_create(
                title=play_data["title"],
                defaults={'description': play_data["description"]}
            )
            if created:
                self.stdout.write(f'Created play: {play}')
                
                for genre_name in play_data["genres"]:
                    genre = Genre.objects.get(name=genre_name)
                    play.genres.add(genre)
                
                for actor_name in play_data["actors"]:
                    first_name, last_name = actor_name.split()
                    actor = Actor.objects.get(first_name=first_name, last_name=last_name)
                    play.actors.add(actor)

        plays = Play.objects.all()
        halls = [hall1, hall2]
        
        for i, play in enumerate(plays):
            for j, hall in enumerate(halls):
                show_time = timezone.now() + timedelta(days=i*7 + j*3, hours=j*2)
                performance, created = Performance.objects.get_or_create(
                    play=play,
                    theatre_hall=hall,
                    show_time=show_time
                )
                if created:
                    self.stdout.write(f'Created performance: {performance}')

        self.stdout.write(
            self.style.SUCCESS('Successfully created sample data!')
        ) 