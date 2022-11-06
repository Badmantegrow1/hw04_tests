from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import Comment, Follow, Group, Post

User = get_user_model()


class GroupModelsTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='Тестовый слаг',
            description='Тестовое описание',
        )

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
        cls.user = User.objects.create_user(username='auth')
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


class FollowModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user1 = User.objects.create_user(username='auth1')
        cls.user2 = User.objects.create_user(username='auth2')
        cls.follow = Follow.objects.create(
            user=cls.user1,
            author=cls.user2,
        )

    def test_follow_str(self):
        """Проверка __str__ у follow."""
        self.assertEqual(
            f'{self.follow.user} подписался на {self.follow.author}',
            str(self.follow))

    def test_follow_verbose_name(self):
        """Проверка verbose_name у follow."""
        field_verboses = {
            'user': 'Пользователь',
            'author': 'Автор',
        }
        for value, expected in field_verboses.items():
            with self.subTest(value=value):
                self.assertEqual(
                    self.follow._meta.get_field(value).verbose_name, expected)


class CommentModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.post = Post.objects.create(
            text='Тестовый пост',
            author=cls.user,
        )
        cls.comment = Comment.objects.create(
            text='Комментарий для поста',
            author=cls.user,
            post=cls.post,
        )

    def test_comment_str(self):
        """Проверка __str__ у сomment."""
        text = self.comment.text
        self.assertEqual(str(self.comment), text[:15])

    def test_comment_verbose_name(self):
        """Проверка verbose_name у сomment."""
        field_verboses = {
            'post': 'Пост',
            'author': 'Автор',
            'text': 'Коментарий',
            'created': 'Создан',
            'updated': 'Обновлен',
            'active': 'Активен',
        }
        for value, expected in field_verboses.items():
            with self.subTest(value=value):
                self.assertEqual(
                    self.comment._meta.get_field(value).verbose_name, expected)
