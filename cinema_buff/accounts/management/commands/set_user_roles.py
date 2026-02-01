from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import UserProfile

class Command(BaseCommand):
    help = 'Set roles for existing users'

    def handle(self, *args, **options):
        # Set user1 as admin
        admin_user = User.objects.get(username='user1')
        admin_user.profile.role = 'admin'
        admin_user.profile.save()
        self.stdout.write(self.style.SUCCESS(f'Set {admin_user.username} as admin'))

        # Set user2 as critic
        critic_user = User.objects.get(username='user2')
        critic_user.profile.role = 'critic'
        critic_user.profile.save()
        self.stdout.write(self.style.SUCCESS(f'Set {critic_user.username} as critic'))

        # Set user3 as critic
        critic_user2 = User.objects.get(username='user3')
        critic_user2.profile.role = 'critic'
        critic_user2.profile.save()
        self.stdout.write(self.style.SUCCESS(f'Set {critic_user2.username} as critic'))

        self.stdout.write(self.style.SUCCESS('User roles updated successfully!'))
