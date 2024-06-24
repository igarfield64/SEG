from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Create hardwired users for testing purposes'

    def handle(self, *args, **options):
        User = get_user_model()

        # Create users with specific usernames and passwords
        users_data = [
            {'username': 'user1', 'password': 'password1'},
            {'username': 'user2', 'password': 'password2'},
            # Add more users as needed
        ]

        for user_data in users_data:
            User.objects.create_user(
                username=user_data['username'],
                password=user_data['password']
            )

        self.stdout.write("Success")