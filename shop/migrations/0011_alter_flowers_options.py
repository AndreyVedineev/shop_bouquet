# Generated by Django 4.2.4 on 2023-09-03 18:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0010_alter_flowers_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='flowers',
            options={'ordering': ['name'], 'permissions': [('is_published', 'Can publish post')], 'verbose_name': 'Букет', 'verbose_name_plural': 'Букеты'},
        ),
    ]