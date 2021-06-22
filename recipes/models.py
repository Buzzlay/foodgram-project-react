from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Exists, OuterRef
from typing import Optional

User = get_user_model()

TAGS = (
    ('Завтрак', 'Завтрак'),
    ('Обед', 'Обед'),
    ('Ужин', 'Ужин')
)


class Ingredient(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name='Название ингредиента',
    )
    dimension = models.CharField(
        max_length=200,
        verbose_name='Мера',
    )

    class Meta:
        ordering = ('title', )
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return f'{self.title}, {self.dimension}'


class Tag(models.Model):
    name = models.CharField(
        max_length=10,
        choices=TAGS
    )
    color = models.CharField(
        max_length=100,
        verbose_name='Цвет тега',
    )
    slug = models.SlugField(
        unique=True
    )

    class Meta:
        ordering = ('id', )
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class RecipeQuerySet(models.QuerySet):
    def with_is_favorite(self, user_id: Optional[int]):
        """Annotate with favorite flag."""
        return self.annotate(is_favorite=Exists(
            Favorite.objects.filter(
                user_id=user_id,
                recipe_id=OuterRef('pk'),
            ),
        ))


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор',
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Название рецепта',
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Тэги',
        related_name='tags'
    )
    image = models.ImageField(
        upload_to='recipes/images/',
        verbose_name='Картинка',
    )
    description = models.TextField(
        verbose_name='Описание',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        through_fields=('recipe', 'ingredient'),
        verbose_name='Ингредиенты',
    )
    time_for_preparing = models.PositiveIntegerField(
        verbose_name='Время приготовления (в минутах)',
        validators=[
            MinValueValidator(1),
        ],
    )
    publication_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
        db_index=True,
    )
    objects = RecipeQuerySet.as_manager()

    class Meta:
        ordering = ('-publication_date', )
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    amount = models.IntegerField(
        verbose_name='Количество',
        validators=[
            MinValueValidator(0),
        ],
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент',
        related_name='ingredient_recipes',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='recipe_ingredients',
    )

    def __str__(self):
        return f'{self.ingredient} в {self.recipe}'

    class Meta:
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецептах'


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Рецепт',
    )

    def __str__(self):
        return f'Избранный {self.recipe} у {self.user}'

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_favorite_user_recipe'
            )
        ]
        verbose_name = 'Объект избранного'
        verbose_name_plural = 'Объекты избранного'


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        related_name='follower',
        on_delete=models.CASCADE
    )
    author = models.ForeignKey(
        User,
        related_name='following',
        on_delete=models.CASCADE
    )

    class Meta:
        models.UniqueConstraint(
            fields=['author', 'user'],
            name='following_unique'
        )

        verbose_name = 'подписка'
        verbose_name_plural = 'подписки'

    def __str__(self):
        return f'{self.user} - подписчик автора - {self.author}'


# class RecipeTag(models.Model):
#     tag = models.ForeignKey(
#         Tag,
#         on_delete=models.CASCADE,
#         verbose_name='Тэг',
#         related_name='tag_recipes',
#     )
#     recipe = models.ForeignKey(
#         Recipe,
#         on_delete=models.CASCADE,
#         verbose_name='Рецепт',
#         related_name='recipe_tags',
#     )
#
#     def __str__(self):
#         return f'{self.recipe} на {self.tag}'
#
#     class Meta:
#         verbose_name = 'Тэг в рецепте'
#         verbose_name_plural = 'Тэги в рецептах'
