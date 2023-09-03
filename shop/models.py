from django.conf import settings
from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Contacts(models.Model):
    name = models.CharField(max_length=150, verbose_name='Имя')
    phone = models.CharField(max_length=35, verbose_name='Телефон')
    message = models.TextField()

    def __str__(self):
        return f'{self.name} {self.phone}'

    class Meta:
        verbose_name = 'Контакт'  # Настройка для наименования одного объекта
        verbose_name_plural = 'Контакты'  # Настройка для наименования набора объектов
        ordering = ['name']


class Category(models.Model):
    name = models.CharField(max_length=150, verbose_name='Категория')
    description = models.TextField(**NULLABLE, verbose_name='Описание')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Категория'  # Настройка для наименования одного объекта
        verbose_name_plural = 'Категории'  # Настройка для наименования набора объектов
        ordering = ['name']


class Flowers(models.Model):
    name = models.CharField(max_length=150, verbose_name='Наименование')
    Imag = models.ImageField(upload_to='products/', verbose_name='Изображение', **NULLABLE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name='Цена')
    date_of_creation = models.DateField(auto_now_add=True, verbose_name='Дата создания')
    last_modified_date = models.DateField(auto_now=True, verbose_name='Дата последнего изменения')
    is_published = models.BooleanField(default=False, verbose_name='Признак публикации ')

    employee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE,
                                 verbose_name='Сотрудник')

    def __str__(self):
        return f'{self.pk} {self.name} {self.category} {self.price} {self.date_of_creation} {self.employee}'

    class Meta:
        verbose_name = 'Букет'  # Настройка для наименования одного объекта
        verbose_name_plural = 'Букеты'  # Настройка для наименования набора объектов
        ordering = ['name']


class Blog(models.Model):
    name = models.CharField(max_length=150, verbose_name='Заголовок')
    slug = models.CharField(max_length=150, verbose_name='Slug')
    content = models.TextField(**NULLABLE, verbose_name='Содержимое')
    image = models.ImageField(upload_to='products/', verbose_name='Превью', **NULLABLE)
    date_of_creation = models.DateField(auto_now_add=True, verbose_name='Дата создания')
    number_of_views = models.IntegerField(default=0, verbose_name='Количество просмотров', **NULLABLE)
    is_published = models.BooleanField(default=False, verbose_name='Признак публикации')

    def __str__(self):
        # Строковое отображение объекта
        return f'{self.name} {self.date_of_creation} {self.is_publication} {self.number_of_views}'

    class Meta:
        verbose_name = 'блог'  # Настройка для наименования одного объекта
        verbose_name_plural = 'Блоги'  # Настройка для наименования набора объектов
        ordering = ['number_of_views']


class Versions(models.Model):
    bouquet = models.ForeignKey(Flowers, on_delete=models.CASCADE, verbose_name='Продукт')
    version_number = models.IntegerField(default=0, verbose_name='Номер версии продукта')
    version_name = models.CharField(max_length=150, verbose_name='Имя версии продукта')
    active_is = models.BooleanField(default=False, verbose_name='Признак активности продукта')

    @property
    def active_version(self):
        return self.versions_set.filter(active_is=True).last()

    def __str__(self):
        return f'{self.bouquet} {self.version_number} {self.version_name}, {self.active_is}'

    class Meta:
        verbose_name = 'Версия букета'  # Настройка для наименования одного объекта
        verbose_name_plural = 'Версии букетов'  # Настройка для наименования набора объектов
