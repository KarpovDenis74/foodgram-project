# Generated by Django 3.2.2 on 2021-07-17 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0005_auto_20210715_1512'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ingredient',
            options={'ordering': ('title',), 'verbose_name': 'Инградиент', 'verbose_name_plural': 'Инградиенты'},
        ),
        migrations.RenameField(
            model_name='ingredient',
            old_name='unit',
            new_name='dimension',
        ),
        migrations.RenameField(
            model_name='recipeingredient',
            old_name='count',
            new_name='amount',
        ),
        migrations.AlterField(
            model_name='recipe',
            name='image',
            field=models.ImageField(blank=True, upload_to='recipes/image/', verbose_name='Изображение готового блюда'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='ingredient',
            field=models.ManyToManyField(through='recipes.RecipeIngredient', to='recipes.Ingredient', verbose_name='Инградиент'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='time_cooking',
            field=models.PositiveIntegerField(verbose_name='Время приготовления,(в минутах)'),
        ),
    ]