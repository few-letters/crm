import random
from django.core.management.base import BaseCommand
from faker import Faker
from website.models import Customer

class Command(BaseCommand):
    help = 'Генерує фейкових клієнтів'

    def add_arguments(self, parser):
        parser.add_argument('total', type=int, help='Кількість клієнтів для створення')

    def handle(self, *args, **kwargs):
        total = kwargs['total']
        fake = Faker('uk_UA')
        
        self.stdout.write('Починаю генерацію...')

        for i in range(total):
            Customer.objects.create(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                email=fake.email(),
                phone=fake.phone_number(),
                country='Ukraine',
                region=fake.region(),
                city=fake.city(),
                address=fake.address()
            )

        self.stdout.write(self.style.SUCCESS(f'Успішно створено {total} клієнтів!'))