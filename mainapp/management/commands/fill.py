from django.core.management.base import BaseCommand
from django.conf import settings

import json

from authapp.models import ShopUser
from mainapp.models import ProducCategory, Product


def load_from_json(file_name):
    with open(f"{settings.BASE_DIR}/json/{file_name}.json", 'r', encoding='utf-8') as json_file:
        return json.load(json_file)


class Command(BaseCommand):

    def handle(self, *args, **options):
        categories = load_from_json('categories')

        ProducCategory.objects.all().delete()
        for category in categories:
            ProducCategory.objects.create(**category)

        products = load_from_json('products')

        Product.objects.all().delete()
        for product in products:
            category_name = product['category']
            category_item = ProducCategory.objects.get(name=category_name)
            product['category'] = category_item
            Product.objects.create(**product)

        ShopUser.objects.create_superuser('django', password='geekbrains', age=18)
