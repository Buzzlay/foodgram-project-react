from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from recipes.models import Ingredient, Favorite, Follow, Recipe


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = (
            'dimension',
            'title',
        )


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = (
            'author',
            'user',
        )
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=['author', 'user']
            )
        ]


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = (
            'user',
            'recipe'
        )
        validators = [
            UniqueTogetherValidator(
                queryset=Favorite.objects.all(),
                fields=['user', 'recipe']
            )
        ]


class PurchasesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = (
            'id',
        )
