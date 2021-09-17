# Generated by Django 3.2.7 on 2021-09-17 06:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num_code', models.PositiveSmallIntegerField(unique=True, verbose_name='Цировой код валюты')),
                ('char_code', models.CharField(max_length=10, unique=True, verbose_name='Буквенный код валюты')),
                ('name', models.CharField(max_length=256, verbose_name='Наименование валюты')),
            ],
            options={
                'verbose_name': 'Иностранная валюта',
                'verbose_name_plural': 'Иностранные валюты',
                'ordering': ['num_code'],
            },
        ),
        migrations.CreateModel(
            name='CurrencyRate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Курс валюты на дату')),
                ('value', models.FloatField(verbose_name='Значение курса валюты')),
                ('nominal', models.PositiveSmallIntegerField(verbose_name='Номинал валюты')),
                ('currency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='currency.currency', verbose_name='валюта')),
            ],
            options={
                'verbose_name': 'Курс валюты',
                'verbose_name_plural': 'Курсы валют',
                'ordering': ['-date'],
            },
        ),
    ]
