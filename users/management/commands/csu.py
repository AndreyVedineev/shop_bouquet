from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        user = User.objects.create(
            email='avedineev@ya.ru',
            first_name='Andrey',
            last_name='Vedineev',
            is_staff=True,
            is_superuser=True

        )
        user.set_password('11122')
        user.save()

