from django import forms
from django.forms import ModelForm

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
                  'image', ]
        labels = {

        }
        help_texts = {
            'name': 'Введите как называется Ваше блюдо',
            'text': 'Введите подробно описание процесса приготовления блюда',
            'time_cooking': 'Сколько по времени готовиться блюдо',
            'image': 'Картинка - хороший способ показать всем свое блюдо'
        }
