from django.test import TestCase
from django.test import Client
from users.models import User
from django.urls import reverse
from django.conf import settings


class TestPosts(TestCase):
    def setUp(self):
        self.client_on = Client()
        self.client_off = Client()
        self.user = User.objects.create(
            username='test_user', email='q@q.com')
        self.user.set_password('123')
        self.user.save()
        self.client_on.force_login(self.user)
        self.clients = (self.client_on, self.client_off,)

    def test_check_debug(self):
        self.assertEqual(settings.DEBUG, False)

    # def test_new_post_user_on(self):
    #     """
    #     Проверка, что зарегистрированный пользователь может создать пост
    #     """
    #     check_list = {'text': 'test text', 'group': self.group1.id, 'author': self.user.id}
    #     response = self.client_on.post(
    #         reverse('new_post'),
    #         data={
    #             'text': check_list['text'],
    #             'group': check_list['group']
    #         }
    #     )
    #     self.assertRedirects(response,
    #         expected_url=reverse('index'),
    #         status_code=302,
    #         target_status_code=200,
    #         msg_prefix='',
    #         fetch_redirect_response=True
    #     )
    #     self.assertEqual(Post.objects.count(), 1)
    #     post = Post.objects.select_related('group', 'author').first()
    #     self.assertEqual(post.text, check_list['text'])
    #     self.assertEqual(post.group, self.group1)
    #     self.assertEqual(post.author, self.user)

    # def test_new_post_user_off(self):
    #     """
    #     Проверка, что незарегистрированный пользователь
    #     редиректится на страницу входа
    #     """
    #     response = self.client_off.get(reverse('new_post'))
    #     reverse1 = reverse('login')
    #     reverse2 = reverse('new_post')
    #     self.assertRedirects(response,
    #         expected_url=f'{reverse1}?next={reverse2}',
    #         status_code=302,
    #         target_status_code=200,
    #         msg_prefix='',
    #         fetch_redirect_response=True
    #     )
    #     post = Post.objects.first()
    #     self.assertFalse(post)

    # def test_view_new_post(self):
    #     """
    #     Проверка отображение нового поста
    #     """
    #     self._create_new_post()
    #     self.post = Post.objects.first()
    #     urls = self._get_url()
    #     for client in self.clients:
    #         for url in urls.values():
    #             response = self.client.get(url)
    #             self.assertContains(
    #                 response,
    #                 self.post.text,
    #                 count=None,
    #                 status_code=200,
    #                 msg_prefix='',
    #                 html=False)

    # def _create_new_post(self):
    #     self.text_check = "test Text 1"
    #     response = self.client_on.post(
    #         reverse('new_post'),
    #         data={
    #             'text': self.text_check,
    #             'group': self.group1.id
    #         }
    #     )

    # def _edit_post(self):
    #     self.text_check = "Измененный пост"
    #     self.response = self.client_on.post(
    #         reverse('post_edit',  kwargs={
    #                 'username': self.user.username, 'post_id': self.post.id}),
    #         data={'username': self.user.username,
    #               'post_id': self.post.id,
    #               })

    # def test_edit_post_user_on(self):
    #     """
    #     Проверка редактирования поста
    #     зарегистрированным пользователем
    #     """
    #     self._create_new_post()
    #     self.post = Post.objects.select_related('author').first()
    #     self._edit_post()
    #     self.assertEqual(self.response.status_code,
    #         200, msg="Проверка редактирования поста"
    #     )
    #     self.post = Post.objects.select_related('author').first()
    #     urls = self._get_url()
    #     check_fields = (
    #         self.post.text, self.post.author.username)
    #     for test_url in urls.values():
    #         response = self.client.get(test_url)
    #         for check_field in check_fields:
    #             self.assertContains(
    #                 response,
    #                 check_field,
    #                 count=None,
    #                 status_code=200,
    #                 msg_prefix='',
    #                 html=False
    #             )

    # def test_edit_post_view(self):
    #     """
    #     Проверка отображения отредактированного поста
    #     зарегистрированным пользователем
    #     """
    #     self._create_new_post()
    #     self.post = Post.objects.select_related('author', 'group').first()
    #     self._edit_post()
    #     self.post = Post.objects.select_related('group').first()
    #     check_fields = (self.post.text, self.post.author.username)
    #     urls = self._get_url()
    #     for test_url in urls.values():
    #         response = self.client.get(test_url)
    #         for check_field in check_fields:
    #             self.assertContains(
    #                 response,
    #                 check_field,
    #                 count=None,
    #                 status_code=200,
    #                 msg_prefix='',
    #                 html=False
    #             )
