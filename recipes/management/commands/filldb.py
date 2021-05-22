from random import randint, sample

from django.core.management import BaseCommand

from recipes.factories import RecipeFactory
from recipes.models import Recipe, Favorite, User
from users.factories import UserFactory

USERS = 100
MAX_RECIPES = 10
MAX_FAVORITES = 20


class Command(BaseCommand):
    """Custom 'filldb' command

    Django commands docs:
    https://docs.djangoproject.com/en/3.1/howto/custom-management-commands/

    """
    help = 'Fill DB with simple data'

    def handle(self, *args, **options):
        users = UserFactory.create_batch(USERS)

        for user in users:
            for _ in range(randint(0, MAX_RECIPES)):
                RecipeFactory(author=user)

        users = User.objects.all()

        for user in users:
            # User cannot favorite his own recipes
            recipes = list(Recipe.objects.exclude(author=user))
            to_favorite = sample(recipes, k=randint(1, MAX_FAVORITES))
            Favorite.objects.bulk_create([
                Favorite(user=user, recipe=recipe) for recipe in to_favorite
            ])
