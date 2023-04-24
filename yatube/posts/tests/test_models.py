from django.test import TestCase

from ..models import Group, Post, User


class PostsModelsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='Тестовый слаг',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовое сообщение',
        )

    def test_models_have_correct_post_text(self):
        """Тест, что в модели Post правильно выполняется __str__."""
        post = self.post
        expected_post = post.text[:15]
        self.assertEqual(expected_post, str(post))

    def test_models_have_correct_goup_title(self):
        """Тест, что в модели Group правильно выполняется __str__."""
        group = self.group
        expected_group = group.title
        self.assertEqual(expected_group, str(group))

    def test_group_verbose_name(self):
        """Тест, что в модели Group правильно выполняется verbose_name."""
        group = self.group
        field_verbose = {
            'title': 'Название группы',
            'slug': 'Адрес для страницы с группой',
            'description': 'Описание',
        }
        for field, expected_value in field_verbose.items():
            with self.subTest(field=field):
                self.assertEqual(
                    group._meta.get_field(field).verbose_name, expected_value
                )

    def test_post_verbose_name(self):
        """Тест, что в модеи Post правильно выполняется verbose_name."""
        post = self.post
        field_verbose = {
            'text': 'Текст сообщения',
            'pub_date': 'Дата публикации',
            'author': 'Автор',
            'group': 'Группа',
        }
        for field, expected_value in field_verbose.items():
            with self.subTest(field=field):
                self.assertEqual(
                    post._meta.get_field(field).verbose_name, expected_value
                )

    def test_group_help_test(self):
        """Тест, что в модели Group правильно выполняется help_text."""
        group = self.group
        field_help_text = {
            'title': 'Введите название группы',
            'slug': 'Адрес заполняется автоматически',
            'description': 'Укажите описание группы',
        }
        for field, expected_value in field_help_text.items():
            with self.subTest(field=field):
                self.assertEqual(
                    group._meta.get_field(field).help_text, expected_value
                )

    def test_post_help_test(self):
        """Тест, что в модели Post правильно выполняется help_text."""
        post = self.post
        field_help_text = {
            'text': 'Введите текст сообщения',
            'pub_date': 'Дата публикации сообщения',
            'author': 'Автор, к которому будет относится сообщение',
            'group': 'Группа, к которой будет относится сообщение',
        }
        for field, expected_value in field_help_text.items():
            with self.subTest(field=field):
                self.assertEqual(
                    post._meta.get_field(field).help_text, expected_value
                )
