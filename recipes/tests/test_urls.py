from django.test import Client, TestCase
from django.urls import reverse
from recipes.models import Ingredient, Recipe, RecipeIngredient
from users.models import User


class TestUrls(TestCase):
    def setUp(self):
        self.username_1, self.email_1 = 'test_client_1', 'q@q.ru'
        self.first_name_1, self.last_name_1 = 'Иван', 'Иванов'
        self.password_1 = '123'
        self.username_2, self.email_2 = 'test_client_2', 'w@w.ru'
        self.first_name_2, self.last_name_2 = 'Петр', 'Петров'
        self.password_2 = '321'
        self.ingr1_title = 'Яйцо куриное'
        self.ingr1_dimension = 'Яйцо куриное 1 сорт'
        self.ingr1 = (Ingredient
                      .objects
                      .create(title=self.ingr1_title,
                              dimension=self.ingr1_dimension))
        self.ingr2_title = 'Молоко коровье'
        self.ingr2_dimension = 'Молоко коровье, 2,5% жирности'
        self.ingr2 = (Ingredient
                      .objects
                      .create(title=self.ingr2_title,
                              dimension=self.ingr2_dimension))
        self.guest_client = Client()
        self.auth_client_1 = Client()
        self.auth_client_2 = Client()
        self.user_1 = (User
                       .objects
                       .create(username=self.username_1,
                               email=self.email_1,
                               last_name=self.last_name_1,
                               first_name=self.first_name_1))
        self.user_1.set_password(self.password_1)
        self.user_1.save()
        self.user_2 = (User
                       .objects
                       .create(username=self.username_2,
                               email=self.email_2,
                               last_name=self.last_name_2,
                               first_name=self.first_name_2))
        self.user_2.set_password(self.password_2)
        self.user_2.save()
        self.recipe1_name = 'Омлет'
        self.recipe1_time_cooking = 10
        self.recipe1 = (Recipe
                        .objects
                        .create(name=self.recipe1_name,
                                author=self.user_1,
                                time_cooking=self.recipe1_time_cooking,
                                ))
        self.ingr1_amount = 100
        (RecipeIngredient
         .objects
         .create(recipes=self.recipe1,
                 ingredient=self.ingr1,
                 amount=self.ingr1_amount))
        self.recipe1.ingredient.add(self.ingr1)
        self.auth_client_1.force_login(self.user_1)
        self.auth_client_2.force_login(self.user_2)
        self.auth_clients = (self.auth_client_1, self.auth_client_2,)
        self.guest_urls = [reverse('index'),
                           reverse('about'),
                           reverse('teсhnologies'),
                           reverse('recipes:shop_list'),
                           reverse('recipes:download_shop_list'),
                           reverse('recipes:view_recipe',
                                   kwargs={'recipe_id': self.recipe1.pk}),
                           reverse('recipes:author',
                                   kwargs={'author_id': self.user_1.pk})]
        self.auth_get_urls = [reverse('recipes:subscriptions'),
                              reverse('recipes:favorites'), ]
        self.auth_post_urls = [reverse('recipes:new'),
                               reverse('recipes:edit_recipe',
                                       kwargs={'recipe_id': self.recipe1.pk}),
                               reverse('recipes:delete_recipe',
                                       kwargs={'recipe_id': self.recipe1.pk}),
                               ]

    def test_guest_urls(self):
        for url in self.guest_urls:
            response = self.guest_client.get(url)
            self.assertEqual(response.status_code,
                             200,
                             msg='Гость может заходить '
                             f'на страницу : {url}')
        for url in self.auth_get_urls:
            response = self.guest_client.get(url)
            self.assertEqual(response.status_code,
                             302,
                             msg='Гость не может заходить '
                                 f'на страницу : {url}')

    def test_auth_urls(self):
        for url in self.auth_get_urls:
            response = self.auth_client_1.get(url)
            self.assertEqual(response.status_code,
                             200,
                             msg='Авторизованный пользователь '
                                 f'может заходить на страницу : {url}')

    # def test_new_recipe(self):
    #     self.ingr3_title = 'Яйцо куриное'
    #     self.ingr3_dimension = 'Яйцо куриное 1 сорт'
    #     self.ingr3 = (Ingredient
    #                   .objects
    #                   .create(title=self.ingr1_title,
    #                           dimension=self.ingr1_dimension))
    #     self.recipe3_name = 'Яичница'
    #     self.recipe3_time_cooking = 5
    #     self.recipe3_text = 'Описание рецепта'
    #     response = (self.auth_client_1
    #                 .post(reverse('recipes:new'),
    #                     data={'name': self.recipe3_name,
    #                           'breakfast': 'on',
    #                           'lunch': 'on',
    #                           'dinner': 'on',
    #                           'nameIngredient_1': self.ingr3.title,
    #                           'valueIngredient_1': 100,
    #                           'time_cooking': self.recipe3_time_cooking,
    #                           'description': self.recipe3_text, })
    #     )
    #     recipes = Recipe.objects.all().count()
    #     self.assertEqual(recipes,
    #                      2, msg='Проверка создания рецепта')
    #     self.assertEqual(response.status_code,
    #                      200, msg='Проверка создания рецепта')
    #     response = (self
    #                 .auth_client_1
    #                 .get(reverse('index')))

    #     self.assertContains(response,
    #                         self.recipe3_name,
    #                         count=None,
    #                         status_code=200,
    #                          msg_prefix='',
    #                         html=False)
