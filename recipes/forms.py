from django.forms import ModelForm
from django import forms
from recipes.models import Recipe


class RecipeForm(ModelForm):
    def clean_text(self):
        if self.cleaned_data['name'] is None:
            raise forms.ValidationError(
                'Пожалуйста, заполните это поле',
                params={'value': self.cleaned_data['name']},
            )
        return self.cleaned_data['name']

    class Meta:
        model = Recipe
        fields = ['name', 'text', 'time_cooking',
                  'image', 'ingredient', 'image']
        labels = {
            'group': 'Рецепт'
        }
        help_texts = {
            'group': 'Название рецепта',
            'text': 'Описание рецепта',
            'time_cooking': 'Время приготовления'
        }
