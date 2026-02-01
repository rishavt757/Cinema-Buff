from django.core.management.base import BaseCommand
from movies.models import Movie, Genre
from decimal import Decimal

class Command(BaseCommand):
    help = 'Add sample movies to the database'

    def handle(self, *args, **options):
        # Get or create genres
        action, _ = Genre.objects.get_or_create(name='Action')
        comedy, _ = Genre.objects.get_or_create(name='Comedy')
        drama, _ = Genre.objects.get_or_create(name='Drama')
        horror, _ = Genre.objects.get_or_create(name='Horror')
        scifi, _ = Genre.objects.get_or_create(name='Science Fiction')

        # Sample movies data
        movies_data = [
            {
                'title': 'The Dark Knight',
                'synopsis': 'When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests of his ability to fight injustice.',
                'release_date': '2008-07-18',
                'genres': [action, drama]
            },
            {
                'title': 'The Hangover',
                'synopsis': 'Three buddies wake up from a bachelor party in Las Vegas with no memory of the previous night and the bachelor missing.',
                'release_date': '2009-06-05',
                'genres': [comedy]
            },
            {
                'title': 'The Conjuring',
                'synopsis': 'Paranormal investigators work to help a family terrorized by a dark presence in their farmhouse.',
                'release_date': '2013-07-19',
                'genres': [horror]
            },
            {
                'title': 'Interstellar',
                'synopsis': 'A team of explorers travel through a wormhole in space in an attempt to ensure humanity\'s survival.',
                'release_date': '2014-11-07',
                'genres': [scifi, drama]
            }
        ]

        for movie_data in movies_data:
            movie, created = Movie.objects.get_or_create(
                title=movie_data['title'],
                defaults={
                    'synopsis': movie_data['synopsis'],
                    'release_date': movie_data['release_date']
                }
            )
            if created:
                movie.genres.set(movie_data['genres'])
                self.stdout.write(self.style.SUCCESS(f'Created movie: {movie.title}'))
            else:
                self.stdout.write(self.style.WARNING(f'Movie already exists: {movie.title}'))

        self.stdout.write(self.style.SUCCESS('Sample movies added successfully!'))
