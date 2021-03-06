# Generated by Django 3.2.2 on 2021-07-15 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0004_auto_20210714_0814'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ingredient',
            options={'verbose_name': 'Инградиент'},
        ),
        migrations.AddField(
            model_name='recipe',
            name='image',
            field=models.ImageField(blank=True, upload_to='posts/', verbose_name='Изображение готового блюда'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='text',
            field=models.TextField(verbose_name='Описание рецепта'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='time_cooking',
            field=models.PositiveIntegerField(verbose_name='Время приготовления'),
        ),
    ]
