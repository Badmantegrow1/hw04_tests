from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import Group, Post

User = get_user_model()


class GroupModelsTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.group = Group.objects.create(title='Тестовая группа')

    def test_group_str_title(self):
        """Проверка, совпадает ли название группы."""
        self.assertEqual(str(self.group), self.group.title)

    def test_group_verbose_name(self):
        """Проверка, совпадают ли verbose_name в полях Group."""
        field_verboses = {
            'title': 'Название',
            'description': 'Описание',
        }
        for value, expected in field_verboses.items():
            with self.subTest(value=value):
                self.assertEqual(
                    self.group._meta.get_field(value).verbose_name, expected
                )

    def test_group_help_text(self):
        """Проверка совпадают ли help_texts в полях Group."""
        help_texts = {
            'title': '',
            'description': '',
        }
        for value, expected in help_texts.items():
            with self.subTest(value=value):
                self.assertEqual(
                    self.group._meta.get_field(value).help_text, expected
                )


class PostModelsTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='person')
        cls.group = Group.objects.create(title='Тестовая группа')
        cls.post = Post.objects.create(
            text='Тестовый пост Тестов',
            author=cls.user,
            group=cls.group,
        )

    def test_post_str_text(self):
        """Проверка, выводятся ли только первые пятнадцать символов поста."""
        text = self.post.text
        self.assertEqual(str(self.post), text[:15])

    def test_post_verbose_name(self):
        """Проверка, совпадают ли verbose_name в полях Post."""
        field_verboses = {
            'text': 'Текст поста',
            'pub_date': 'Дата публикации',
            'author': 'Автор',
            'group': 'Группа',
        }
        for value, expected in field_verboses.items():
            with self.subTest(value=value):
                self.assertEqual(
                    self.post._meta.get_field(value).verbose_name, expected
                )

    def test_post_help_text(self):
        """Проверка, совпадают ли help_texts в полях Post."""
        help_texts = {
            'text': 'Введите текст поста',
            'pub_date': '',
            'author': '',
            'group': 'Группа, к которой будет относиться пост',
        }
        for value, expected in help_texts.items():
            with self.subTest(value=value):
                self.assertEqual(
                    self.post._meta.get_field(value).help_text, expected
                )
