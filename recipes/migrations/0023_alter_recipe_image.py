# Generated by Django 3.2.2 on 2021-08-04 20:21

from django.db import migrations, models
import recipes.models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0020_alter_recipeingredient_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='image',
            field=models.ImageField(blank=True, upload_to='recipes/image/', verbose_name='Изображение готового блюда'),
        ),
    ]