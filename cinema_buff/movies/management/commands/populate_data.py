from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from movies.models import Genre, Movie, Rating, Review
from communities.models import Community, CommunityMember
from accounts.models import UserProfile
from datetime import date, timedelta
import random

class Command(BaseCommand):
    help = 'Populate the database with sample data'

    def handle(self, *args, **options):
        # Create sample users
        users = []
        for i in range(10):
            username = f'user{i+1}'
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(
                    username=username,
                    email=f'{username}@cinemabuff.com',
                    password='password123'
                )
                users.append(user)
                self.stdout.write(f'Created user: {username}')
            else:
                users.append(User.objects.get(username=username))

        # Create genres
        genres_data = [
            {'name': 'Action', 'description': 'Action-packed movies with stunts and explosions'},
            {'name': 'Comedy', 'description': 'Funny movies that make you laugh'},
            {'name': 'Drama', 'description': 'Serious movies with emotional stories'},
            {'name': 'Horror', 'description': 'Scary movies that give you chills'},
            {'name': 'Romance', 'description': 'Love stories and romantic movies'},
            {'name': 'Sci-Fi', 'description': 'Science fiction movies with futuristic themes'},
            {'name': 'Thriller', 'description': 'Suspenseful movies that keep you on edge'},
            {'name': 'Animation', 'description': 'Animated movies for all ages'},
            {'name': 'Crime', 'description': 'Movies about criminal activities and investigations'},
            {'name': 'Adventure', 'description': 'Exciting movies with journeys and exploration'},
        ]

        genres = []
        for genre_data in genres_data:
            genre, created = Genre.objects.get_or_create(
                name=genre_data['name'],
                defaults={'description': genre_data['description']}
            )
            genres.append(genre)
            if created:
                self.stdout.write(f'Created genre: {genre.name}')

        # Create communities for each genre
        for genre in genres:
            community, created = Community.objects.get_or_create(
                genre=genre,
                defaults={
                    'name': f'{genre.name} Lovers',
                    'description': f'A community for fans of {genre.name} movies'
                }
            )
            if created:
                self.stdout.write(f'Created community: {community.name}')

        # Create sample movies
        movies_data = [
            {
                'title': 'The Dark Knight',
                'synopsis': 'When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests of his ability to fight injustice.',
                'release_date': date(2008, 7, 18),
                'genres': ['Action', 'Drama', 'Thriller']
            },
            {
                'title': 'Inception',
                'synopsis': 'A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O.',
                'release_date': date(2010, 7, 16),
                'genres': ['Action', 'Sci-Fi', 'Thriller']
            },
            {
                'title': 'The Shawshank Redemption',
                'synopsis': 'Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.',
                'release_date': date(1994, 9, 23),
                'genres': ['Drama']
            },
            {
                'title': 'Pulp Fiction',
                'synopsis': 'The lives of two mob hitmen, a boxer, a gangster and his wife intertwine in four tales of violence and redemption.',
                'release_date': date(1994, 10, 14),
                'genres': ['Crime', 'Drama']
            },
            {
                'title': 'The Matrix',
                'synopsis': 'A computer programmer discovers that reality as he knows it is a simulation created by machines, and joins a rebellion to break free.',
                'release_date': date(1999, 3, 31),
                'genres': ['Action', 'Sci-Fi']
            },
            {
                'title': 'Forrest Gump',
                'synopsis': 'The presidencies of Kennedy and Johnson, the Vietnam War, and the Watergate scandal unfold from the perspective of an Alabama man with an IQ of 75.',
                'release_date': date(1994, 7, 6),
                'genres': ['Drama', 'Romance']
            },
            {
                'title': 'The Godfather',
                'synopsis': 'The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son.',
                'release_date': date(1972, 3, 24),
                'genres': ['Crime', 'Drama']
            },
            {
                'title': 'Toy Story',
                'synopsis': 'A cowboy doll is threatened by a new spaceman figure, but they both must overcome their differences when they are separated from their owner.',
                'release_date': date(1995, 11, 22),
                'genres': ['Animation', 'Adventure', 'Comedy']
            },
            {
                'title': 'The Avengers',
                'synopsis': 'Earth mightiest heroes must come together and learn to fight as a team if they are to stop the mischievous Loki and his alien army from enslaving humanity.',
                'release_date': date(2012, 5, 4),
                'genres': ['Action', 'Adventure', 'Sci-Fi']
            },
            {
                'title': 'Finding Nemo',
                'synopsis': 'After his son is captured in the Great Barrier Reef and taken to Sydney, a timid clownfish sets out on a journey to bring him home.',
                'release_date': date(2003, 5, 30),
                'genres': ['Animation', 'Adventure', 'Comedy']
            }
        ]

        movies = []
        for movie_data in movies_data:
            movie, created = Movie.objects.get_or_create(
                title=movie_data['title'],
                defaults={
                    'synopsis': movie_data['synopsis'],
                    'release_date': movie_data['release_date']
                }
            )
            
            if created:
                # Add genres to movie
                for genre_name in movie_data['genres']:
                    genre = Genre.objects.get(name=genre_name)
                    movie.genres.add(genre)
                
                movies.append(movie)
                self.stdout.write(f'Created movie: {movie.title}')
            else:
                movies.append(movie)

        # Create ratings and reviews
        for movie in movies:
            for user in random.sample(users, random.randint(3, 8)):
                # Create rating
                score = random.randint(1, 5)
                rating, created = Rating.objects.get_or_create(
                    user=user,
                    movie=movie,
                    defaults={'score': score}
                )
                if created:
                    self.stdout.write(f'Created rating: {user.username} - {movie.title} - {score}')

                # Create review (70% chance)
                if random.random() < 0.7:
                    review_titles = ['Amazing!', 'Great movie', 'Not bad', 'Could be better', 'Excellent!']
                    review_contents = [
                        'This movie was fantastic! I really enjoyed every minute of it.',
                        'A solid film with good performances and an interesting story.',
                        'It was okay, but I expected more from the cast and director.',
                        'Decent entertainment, but nothing groundbreaking.',
                        'One of the best movies I have seen this year. Highly recommended!'
                    ]
                    
                    Review.objects.get_or_create(
                        user=user,
                        movie=movie,
                        defaults={
                            'title': random.choice(review_titles),
                            'content': random.choice(review_contents)
                        }
                    )

        # Join users to communities
        for user in users:
            # Join 2-4 random communities
            communities = Community.objects.all()
            for community in random.sample(list(communities), random.randint(2, 4)):
                CommunityMember.objects.get_or_create(
                    user=user,
                    community=community
                )

        self.stdout.write(self.style.SUCCESS('Sample data populated successfully!'))
