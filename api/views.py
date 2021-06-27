from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from recipes.models import Favorite, Follow, Recipe, Ingredient
from .serializers import (
    IngredientSerializer,
    FollowSerializer,
    FavoriteSerializer,
    PurchasesSerializer,
)


class AddToFavorites(APIView):

    def post(self, request, format=None):
        """Add a Recipe to Favorites of a User."""
        recipe_id = request.data['id']
        user = self.request.user,
        serializer = FavoriteSerializer(
            data={
                'recipe': recipe_id,
                'user': user[0].id
            })
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        """Remove a Recipe from User's Favorite"""
        Favorite.objects.filter(recipe_id=id, user=self.request.user).delete()
        return Response({'success': True}, status=status.HTTP_200_OK)


class AddToFollows(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request, format=None):
        """Subscribe to the author."""
        author_id = int(self.request.data['id'])
        user = self.request.user
        serializer = FollowSerializer(
            data={
                'author': author_id,
                'user': user.id
            })
        if serializer.is_valid() and user.id != author_id:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, author_id):
        """Unsubscribe from author."""
        get_object_or_404(
            Follow,
            user=self.request.user,
            author=author_id,
        ).delete()
        return Response({'success': True}, status=status.HTTP_200_OK)


class Purchases(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        """Add Recipe to Purchases."""
        recipe = get_object_or_404(Recipe, id=self.request.data['id'])
        cart = request.session.get('cart')
        serializer = PurchasesSerializer(
            data={
                'id': recipe.id,
            }
        )
        if recipe.id not in cart and serializer.is_valid():
            cart[recipe.id] = recipe.name
            request.session.modified = True
            return Response({'success': True}, status=status.HTTP_200_OK)
        return Response({'success': False}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, recipe_id):
        """Delete Recipe from Purchases."""
        recipe_id = str(recipe_id)
        cart = self.request.session['cart']
        if recipe_id in cart:
            del cart[recipe_id]
        request.session.modified = True
        return Response({'success': True}, status=status.HTTP_200_OK)


class IngredientView(ListAPIView):
    serializer_class = IngredientSerializer

    def get_queryset(self):
        """Get ingredients list."""
        title = self.request.GET.get('query', '')
        return Ingredient.objects.filter(title__icontains=title)
