import json

from django.conf import settings
from django.core.cache import cache

from shop.models import Category


def write_json_message(data):
    """
    Для контроллера contacts
    :param data:
    :return: -
    """
    with open('data_massage.json', 'w', encoding='UTF-8') as fp:
        json.dump(data, fp, ensure_ascii=False)


def get_category_cache(context):
    if settings.CACHE_ENABLED:
        # Проверяем включенность кеша
        key = 'category_list'  # Создаем ключ для хранения
        category_list = cache.get(key)  # Пытаемся получить данные
        if category_list is None:
            # Если данные не были получены из кеша, то выбираем из БД и записываем в кеш
            category_list = Category.objects.all()
            cache.set(key, category_list)
    else:
        # Если кеш не был подключен, то просто обращаемся к БД
        category_list = Category.objects.all()

    context['category_list'] = category_list

    return context
