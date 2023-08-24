# python3 manage.py fill.py


from django.core.management import BaseCommand
from django.core.management.color import no_style
from django.db import connection

from shop.models import Category, Flowers

sequence_sql = connection.ops.sequence_reset_sql(no_style(), [Category, Flowers])
with connection.cursor() as cursor:
    for sql in sequence_sql:
        cursor.execute(sql)


class Command(BaseCommand):

    def handle(self, *args, **options):
        category_list = [
            {'name': 'Для мамы', 'description': 'Теплые и нежные тона!'},
            {'name': 'Свадебный', 'description': 'Для невест и подружек!'},
            {'name': 'Праздничный', 'description': 'Для любого события в жизни!'},
            {'name': 'На каждый день', 'description': 'Можно подарить просто так, или в знак любви и признания!'},
        ]

        category_for_create = []
        for item in category_list:
            category_for_create.append(Category(**item))

        Category.objects.bulk_create(category_for_create)

        pk_1 = Category.objects.get(pk=1)
        pk_2 = Category.objects.get(pk=2)
        pk_3 = Category.objects.get(pk=3)
        pk_4 = Category.objects.get(pk=4)

        flowers_list = [
            {'name': "Ах, это свадьба!", 'category': pk_3, 'price': 5000},
            {'name': "Дорогой!", 'category': pk_1, 'price': 7000},
            {'name': "Единственной!", 'category': pk_3, 'price': 4500},
            {'name': "Каждый день!", 'category': pk_1, 'price': 3500},
            {'name': "Мега Юбиляр!", 'category': pk_2, 'price': 4500},
            {'name': "Моей маме!", 'category': pk_4, 'price': 3800},
            {'name': "От детей и внуков!", 'category': pk_4, 'price': 2000},
            {'name': "Хорошие цветы!", 'category': pk_1, 'price': 3000},
            {'name': "Юбилейный!", 'category': pk_2, 'price': 4900},
        ]

        flowers_for_create = []
        for item in flowers_list:
            flowers_for_create.append(Flowers(**item))

        Flowers.objects.bulk_create(flowers_for_create)
