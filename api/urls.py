from django.urls import path

from api.views import AddToFavorites, AddToFollows, Purchases, IngredientView

urlpatterns = [
    path(
        'favorites/',
        AddToFavorites.as_view(),
        name='add_favorites',
    ),
    path(
        'favorites/<int:id>/',
        AddToFavorites.as_view(),
        name='delete_favorites',
    ),
    path('ingredients/',
         IngredientView.as_view(),
         name='ingredients',
         ),
    path(
        'subscriptions/',
        AddToFollows.as_view(),
        name='follow',
    ),
    path(
        'subscriptions/<int:author_id>/',
        AddToFollows.as_view(),
        name='unfollow',
    ),
    path(
        'purchases/',
        Purchases.as_view(),
        name='add_purchase'
    ),
    path(
        'purchases/<int:recipe_id>/',
        Purchases.as_view(),
        name='delete_purchase'
    ),
]
