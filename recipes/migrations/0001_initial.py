from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(
                    auto_created=True,
                    primary_key=True,
                    serialize=False,
                    verbose_name='ID'
                )),
                ('title', models.CharField(
                    max_length=200,
                    verbose_name='Название ингредиента'
                )),
                ('dimension', models.CharField(
                    max_length=200,
                    verbose_name='Мера'
                )),
            ],
            options={
                'verbose_name': 'Ингредиент',
                'verbose_name_plural': 'Ингредиенты',
                'ordering': ('title',),
            },
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(
                    auto_created=True,
                    primary_key=True,
                    serialize=False,
                    verbose_name='ID'
                )),
                ('name', models.CharField(
                    max_length=200,
                    verbose_name='Название рецепта'
                )),
                ('image', models.ImageField(
                    upload_to='recipes/images/',
                    verbose_name='Картинка'
                )),
                ('description', models.TextField(verbose_name='Описание')),
                ('time_for_preparing', models.PositiveIntegerField(
                    validators=[django.core.validators.MinValueValidator(1)],
                    verbose_name='Время приготовления (в минутах)'
                )),
                ('publication_date', models.DateTimeField(
                    auto_now_add=True,
                    db_index=True,
                    verbose_name='Дата публикации'
                )),
                ('author', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='recipes',
                    to=settings.AUTH_USER_MODEL,
                    verbose_name='Автор'
                )),
            ],
            options={
                'verbose_name': 'Рецепт',
                'verbose_name_plural': 'Рецепты',
                'ordering': ('-publication_date',),
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(
                    auto_created=True,
                    primary_key=True,
                    serialize=False,
                    verbose_name='ID'
                )),
                ('name', models.CharField(
                    choices=[
                        ('Завтрак', 'Завтрак'),
                        ('Обед', 'Обед'),
                        ('Ужин', 'Ужин')
                    ],
                    max_length=10,
                    verbose_name='Имя тэга'
                )),
                ('color', models.CharField(
                    max_length=100,
                    verbose_name='Цвет тега'
                )),
                ('slug', models.SlugField(
                    unique=True,
                    verbose_name='Слаг тэга'
                )),
            ],
            options={
                'verbose_name': 'Тег',
                'verbose_name_plural': 'Теги',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='RecipeIngredient',
            fields=[
                ('id', models.BigAutoField(
                    auto_created=True,
                    primary_key=True,
                    serialize=False,
                    verbose_name='ID'
                )),
                ('amount', models.IntegerField(
                    validators=[django.core.validators.MinValueValidator(0)],
                    verbose_name='Количество'
                )),
                ('ingredient', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='ingredient_recipes',
                    to='recipes.ingredient',
                    verbose_name='Ингредиент'
                )),
                ('recipe', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='recipe_ingredients',
                    to='recipes.recipe',
                    verbose_name='Рецепт'
                )),
            ],
            options={
                'verbose_name': 'Ингредиент в рецепте',
                'verbose_name_plural': 'Ингредиенты в рецептах',
            },
        ),
        migrations.AddField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(
                through='recipes.RecipeIngredient',
                to='recipes.Ingredient',
                verbose_name='Ингредиенты'
            ),
        ),
        migrations.AddField(
            model_name='recipe',
            name='tags',
            field=models.ManyToManyField(
                related_name='recipes',
                to='recipes.Tag',
                verbose_name='Тэги'
            ),
        ),
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('id', models.BigAutoField(
                    auto_created=True,
                    primary_key=True,
                    serialize=False,
                    verbose_name='ID'
                )),
                ('author', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='following',
                    to=settings.AUTH_USER_MODEL,
                    verbose_name='Автор'
                )),
                ('user', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='follower',
                    to=settings.AUTH_USER_MODEL,
                    verbose_name='Подписчик'
                )),
            ],
            options={
                'verbose_name': 'подписка',
                'verbose_name_plural': 'подписки',
            },
        ),
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.BigAutoField(
                    auto_created=True,
                    primary_key=True,
                    serialize=False,
                    verbose_name='ID'
                )),
                ('recipe', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='favorites',
                    to='recipes.recipe',
                    verbose_name='Рецепт'
                )),
                ('user', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='favorites',
                    to=settings.AUTH_USER_MODEL,
                    verbose_name='Пользователь'
                )),
            ],
            options={
                'verbose_name': 'Объект избранного',
                'verbose_name_plural': 'Объекты избранного',
            },
        ),
        migrations.AddConstraint(
            model_name='favorite',
            constraint=models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_favorite_user_recipe'
            ),
        ),
    ]
