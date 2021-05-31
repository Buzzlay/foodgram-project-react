from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from recipes.models import Favorite, Follow, User


class AddToFavorites(APIView):
    """Add a Recipe to Favorites of a User."""

    def post(self, request, format=None):
        Favorite.objects.get_or_create(
            user=request.user,
            recipe_id=request.data['id']
        )

        return Response({'success': True}, status=status.HTTP_200_OK)


class RemoveFromFavorite(APIView):
    """Remove a Recipe from User's Favorite"""

    def delete(self, request, id, format=None):
        Favorite.objects.filter(recipe_id=id, user=request.user).delete()
        return Response({'success': True}, status=status.HTTP_200_OK)


class AddToFollows(APIView):
    """Subscribe to the author."""

    def post(self, request):
        author = get_object_or_404(User, id=request.data['id'])
        Follow.objects.get_or_create(
            user=self.request.user,
            author=author,
        )
        return Response({'success': True}, status=status.HTTP_200_OK)

    """Unsubscribe from author."""

    def delete(self, request, author_id):
        get_object_or_404(
            Follow,
            user=request.user,
            author=author_id,
        ).delete()
        return Response({'success': True}, status=status.HTTP_200_OK)
