import sys

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from api.models import FacebookPage


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            '-a',
            '-access_token',
            dest='access_token',
            type=str
        )
        parser.add_argument(
            '-e',
            '-email',
            type=str,
            dest='email'
        )

    def handle(self, *args, **options):
        access_token = options.get('access_token')
        email = options.get('email')
        if not access_token or not email:
            self.stdout.write(self.style.ERROR(
                'Access token and email should be supplied'
            ))
            sys.exit(1)
        user = User.objects.create(email=email)
        FacebookPage.objects.create(
            access_token=access_token,
            owner=user
        )
