from http import HTTPStatus

from django.test import Client, TestCase
from django.urls import reverse
from posts.models import Group, Post, User


class PostCreateFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.author = User.objects.create_user(username='Test_name')
        cls.group = Group.objects.create(
            title='test_name_group',
            slug='test_slug',
        )
        cls.group2 = Group.objects.create(
            title='test_name_group_two',
            slug='test_slug_two',
        )
        cls.post = Post.objects.create(
            text='test_text_form',
            author=cls.author,
            group=cls.group,
        )
        cls.url_create = reverse('posts:post_create')

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.author)

    def test_authorized_create_post(self):
        """Соответствующая форма создает запись в Post."""
        posts_count = Post.objects.count()
        form = {
            'text': self.post.text,
            'group': self.group.id,
        }
        self.authorized_client.post(
            reverse('posts:post_create'),
            data=form,
            follow=True
        )
        # Проверяем увеличилось ли число постов
        self.assertEqual(
            Post.objects.count(),
            posts_count + 1,
        )
        # Проверяем создались ли запись
        self.assertTrue(
            Post.objects.filter(
                text=self.post.text,
                group=self.group.id,
            ).exists()
        )

    def test_guest_create_post(self):
        """Тест, что при создании поста анонимным пользователем количество постов
        в базе данных не меняется.
        """
        posts_count = Post.objects.count()
        form = {
            'text': self.post.text,
            'group': self.group.id,
        }
        response = self.client.post(
            reverse('posts:post_create'),
            data=form,
            follow=True,
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertRedirects(response, f'/auth/login/?next={self.url_create}')
        self.assertEqual(Post.objects.count(), posts_count)

    def test_edit_post(self):
        """Соответствующая форма редактирует запись в Post."""
        form = {
            'text': 'Отредактированный текст поста',
            'group': self.group2.id,
        }
        response = self.authorized_client.post(
            reverse('posts:post_edit', kwargs={'post_id': self.post.id}),
            data=form,
            follow=True,
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTrue(
            Post.objects.filter(
                text=form['text'],
                group=form['group'],
            ).exists()
        )
