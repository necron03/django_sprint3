import pytest
from blog.models import Post
from django.db.models import (
    BooleanField, CharField, DateTimeField, ForeignKey, TextField)
from django.db.utils import IntegrityError

from tests.conftest import _TestModelAttrs

pytestmark = [
    pytest.mark.django_db,
]


@pytest.mark.parametrize(
    ('field', 'type', 'params'), [
        ('title', CharField, {'max_length': 256}),
        ('text', TextField, {}),
        ('pub_date', DateTimeField, {'auto_now': False, 'auto_now_add': False}),
        ('author', ForeignKey, {'null': False}),
        ('location', ForeignKey, {'null': True}),
        ('category', ForeignKey, {'null': True}),  # проверить в notion
        ('is_published', BooleanField, {'default': True}),
        ('created_at', DateTimeField, {'auto_now_add': True}),
    ])
class TestCategoryModelAttrs(_TestModelAttrs):

    @property
    def model(self):
        return Post


def test_author_on_delete(posts_with_author):
    author = posts_with_author[0].author
    author_id = author.id  # Сохраняем ID до удаления

    try:
        author.delete()
    except IntegrityError:
        raise AssertionError(
            'Проверьте, что значение атрибута `on_delete` '
            'поля `author` в модели `Post` соответствует заданию.'
        )
    assert not Post.objects.filter(author_id=author_id).exists(), (
        'Проверьте, что значение атрибута `on_delete` '
        'поля `author` в модели `Post` соответствует заданию.'
    )


def test_location_on_delete(posts_with_published_locations):
    location = posts_with_published_locations[0].location
    location_id = location.id  # Сохраняем ID до удаления

    try:
        location.delete()
    except IntegrityError:
        raise AssertionError(
            'Проверьте, что значение атрибута `on_delete` '
            'поля `location` в модели `Post` соответствует заданию.'
        )
    # Для SET_NULL посты должны остаться, но location_id должен стать NULL
    posts_after_delete = Post.objects.filter(location_id=location_id)
    assert not posts_after_delete.exists(), (
        'Проверьте, что значение атрибута `on_delete` '
        'поля `location` в модели `Post` соответствует заданию.'
    )

    # Проверяем, что посты все еще существуют с NULL в location
    original_post_ids = [post.id for post in posts_with_published_locations]
    posts_still_exist = Post.objects.filter(id__in=original_post_ids).exists()
    assert posts_still_exist, (
        'Посты не должны удаляться при удалении локации'
    )