from django import forms
from django.conf import settings
from django.test import Client, TestCase
from django.urls import reverse

from ..forms import PostForm
from ..models import Group, Post, User


class PostViewsTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.author = User.objects.create_user(
            username='Test_name',
            email='test@gmail.com',
        )
        cls.group = Group.objects.create(
            title='Первая группа',
            slug='test_slug',
            description='Тестовое описание',
        )
        cls.group2 = Group.objects.create(
            title='Вторая группа',
            slug='test_slug_two',
            description='Описание второй группы'
        )
        cls.post = Post.objects.create(
            author=cls.author,
            text="Тестовый пост",
            group=cls.group,
        )
        cls.new_post = Post.objects.create(
            author=cls.author,
            text='Новый пост 2',
            group=cls.group,
        )
        cls.post_create_urls = {
            reverse('posts:index'): 'posts/index.html',
            reverse(
                'posts:profile', kwargs={'username': cls.author.username}):
                    'posts/profile.html',
            reverse(
                'posts:group_list', kwargs={'slug': cls.group.slug}):
                    'posts/group_list.html',
        }
        cls.template_page_name = {
            reverse(
                'posts:post_detail', kwargs={'post_id': cls.post.pk}):
                    'posts/post_detail.html',
            reverse(
                'posts:post_create'): 'posts/post_create.html',
            reverse(
                'posts:post_edit', kwargs={'post_id': cls.post.pk}):
                    'posts/post_create.html',
            **cls.post_create_urls,
        }
        cls.form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.author)

    def test_pages_uses_correct_template(self):
        """Тест шаблонов."""
        for reverse_name, template in self.template_page_name.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def assert_post(self, post):
        """Функция проверки контекста"""
        with self.subTest(post=post):
            self.assertEqual(
                post.text, self.post.text)
            self.assertEqual(
                post.author, self.post.author)
            self.assertEqual(
                post.group, self.post.group)

    def test_index_page_show_correct_context(self):
        """Тест index на наличие верного context."""
        response = self.authorized_client.get(reverse('posts:index'))
        self.assert_post(response.context['page_obj'][0])

    def test_group_list_page_show_correct_context(self):
        """Тест group_list на наличие верного context."""
        response = self.authorized_client.get(
            reverse(
                'posts:group_list',
                kwargs={'slug': self.group.slug}
            )
        )
        self.assertEqual(response.context['group'], self.group)
        self.assert_post(response.context['page_obj'][0])

    def test_profile_page_show_correct_context(self):
        """Тест profile на наличие верного context."""
        response = self.authorized_client.get(
            reverse(
                'posts:profile',
                kwargs={'username': self.author}
            )
        )
        self.assertEqual(response.context['author'], self.author)
        self.assert_post(response.context['page_obj'][0])

    def test_detail_page_show_correct_context(self):
        """Тест post_detail на наличие верного context."""
        response = self.authorized_client.get(
            reverse(
                'posts:post_detail',
                kwargs={'post_id': self.post.id}
            )
        )
        self.assert_post(response.context['post'])

    def test_post_create_page_show_correct_context(self):
        """Тест шаблона post_create на наличие верного context."""
        response = self.authorized_client.get(reverse('posts:post_create'))
        form = response.context.get('form')
        self.assertIsInstance(form, PostForm)
        for value, expected in self.form_fields.items():
            with self.subTest(value=value):
                form_field = form.fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_post_edit_page_show_correct_context(self):
        """Тест шаблона post_edit на наличие верного context."""
        response = self.authorized_client.get(reverse(
            'posts:post_edit', kwargs={'post_id': self.post.pk}))
        form = response.context.get('form')
        self.assertIsInstance(form, PostForm)
        for value, expected in self.form_fields.items():
            with self.subTest(value=value):
                form_field = form.fields.get(value)
                self.assertIsInstance(form_field, expected)
                self.assertTrue(response.context.get('is_edit'))


class PostViewsTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.author = User.objects.create_user(
            username='Test_name',
            email='test@gmail.com',
            password='password',
        )
        cls.group = Group.objects.create(
            title='Первая группа',
            slug='test_slug',
            description='Тестовое описание',
        )
        cls.group2 = Group.objects.create(
            title='Вторая группа',
            slug='test_slug_two',
            description='Описание второй группы'
        )
        cls.post = Post.objects.create(
            author=cls.author,
            text="Тестовый пост",
            group=cls.group,
        )
        cls.post_create_urls = {
            reverse('posts:index'): 'posts/index.html',
            reverse(
                'posts:profile', kwargs={'username': cls.author.username}):
                    'posts/profile.html',
            reverse(
                'posts:group_list', kwargs={'slug': cls.group.slug}):
                    'posts/group_list.html',
        }

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.author)

    def test_new_post_is_shown(self):
        """Протестируйте, что если при создании поста указать группу,
        то этот пост появляется:
        -- на странице выбранной группы,
        -- в профайле пользователя,
        -- на главной странице сайта.
        """
        for url in self.post_create_urls:
            with self.subTest(value=url):
                response = self.client.get(url)
                self.assertIn(self.post, response.context['page_obj'])

    def test_new_post_for_your_group(self):
        """Тест, что этот пост не попал в группу,
        не свойственной ему.
        """
        response = self.client.get(
            reverse('posts:group_list', kwargs={'slug': self.group2.slug})
        )
        self.assertNotIn(self.post, response.context['page_obj'])


class PaginatorViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.author = User.objects.create(
            username='auth',
        )
        cls.group = Group.objects.create(
            title='Тестовое название группы',
            slug='test_slug',
            description='Тестовое описание группы',
        )
        cls.posts_on_first_page = settings.POSTS_PER_PAGE
        cls.posts_on_second_page = 3
        for i in range(cls.posts_on_second_page + cls.posts_on_first_page):
            Post.objects.create(
                text=f'Пост №{i}',
                author=cls.author,
                group=cls.group
            )

    def test_paginator_on_pages(self):
        """Тест пагинации страниц."""
        url_pages = [
            reverse('posts:index'),
            reverse('posts:group_list', kwargs={'slug': self.group.slug}),
            reverse('posts:profile',
                    kwargs={'username': self.author.username}),
        ]
        for reverse_page in url_pages:
            with self.subTest(reverse_page=reverse_page):
                self.assertEqual(len(self.client.get(
                    reverse_page).context.get('page_obj')),
                    self.posts_on_first_page
                )
                self.assertEqual(len(self.client.get(
                    reverse_page + '?page=2').context.get('page_obj')),
                    self.posts_on_second_page
                )
