# Generated by Django 4.2.4 on 2023-08-28 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_contacts_alter_category_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Наименование')),
                ('slug', models.CharField(max_length=150, verbose_name='Slug')),
                ('content', models.TextField(blank=True, null=True, verbose_name='Содержимое')),
                ('image', models.ImageField(blank=True, null=True, upload_to='products/', verbose_name='Превью')),
                ('date_of_creation', models.DateField(auto_now_add=True, verbose_name='Дата создания')),
                ('is_publication', models.BooleanField(default=True, verbose_name='Признак публикации')),
                ('number_of_views', models.IntegerField(blank=True, default=0, null=True, verbose_name='Количество просмотров')),
            ],
            options={
                'verbose_name': 'блог',
                'verbose_name_plural': 'Блоги',
                'ordering': ['number_of_views'],
            },
        ),
        migrations.AlterModelOptions(
            name='contacts',
            options={'ordering': ['name'], 'verbose_name': 'Контакт', 'verbose_name_plural': 'Контакты'},
        ),
    ]