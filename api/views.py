from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from recipes.models import Favorite, Follow, User, Recipe


class AddToFavorites(APIView):

    def post(self, request, format=None):
        """Add a Recipe to Favorites of a User."""
        Favorite.objects.get_or_create(
            user=request.user,
            recipe_id=request.data['id']
        )

        return Response({'success': True}, status=status.HTTP_200_OK)

    def delete(self, request, id, format=None):
        """Remove a Recipe from User's Favorite"""
        Favorite.objects.filter(recipe_id=id, user=request.user).delete()
        return Response({'success': True}, status=status.HTTP_200_OK)


class AddToFollows(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        """Subscribe to the author."""
        author = get_object_or_404(User, id=request.data['id'])
        Follow.objects.get_or_create(
            user=self.request.user,
            author=author,
        )
        return Response({'success': True}, status=status.HTTP_200_OK)

    def delete(self, request, author_id):
        """Unsubscribe from author."""
        get_object_or_404(
            Follow,
            user=request.user,
            author=author_id,
        ).delete()
        return Response({'success': True}, status=status.HTTP_200_OK)


class Purchases(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        """Add Recipe to Purchases."""
        recipe = get_object_or_404(Recipe, id=request.data['id'])
        cart = request.session['cart']
        if recipe.id not in cart.keys():
            cart[recipe.id] = {
                'name': recipe.name,
                'image': recipe.image.url,
                'cook_time': recipe.time_for_preparing,
            }
            request.session.modified = True
        return Response({'success': True}, status=status.HTTP_200_OK,)

    def delete(self, request, recipe_id):
        """Delete Recipe from Purchases."""
        recipe_id = str(recipe_id)
        cart = request.session['cart']
        if recipe_id in cart.keys():
            del request.session['cart'][recipe_id]
        request.session.modified = True
        return Response({'success': True}, status=status.HTTP_200_OK)
