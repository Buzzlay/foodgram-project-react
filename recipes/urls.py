from django.urls import path, include

from . import views


urlpatterns = [
    path(
        '',
        views.IndexView.as_view(),
        name='index'
    ),
    # path(
    #     '<slug:tag_slug>',
    #     views.recipes_by_tag,
    #     name='recipes_list_by_tag'
    # ),
    path('api/', include('api.urls')),
    path(
        'download_cart/',
        views.download_cart,
        name='download_cart'
    ),
    path(
        'favorites/',
        views.FavoriteView.as_view(),
        name='favorites'
    ),
    path(
        'profiles/<str:username>/',
        views.ProfileView.as_view(),
        name='profile'
    ),
    path(
        'recipes/<int:pk>/',
        views.RecipeDetailView.as_view(),
        name='recipe'
    ),
    path(
        'recipes/<int:recipe_id>/edit/',
        views.recipe_edit_or_create,
        name='edit'
    ),
    path(
        'recipes/<int:recipe_id>/delete/',
        views.recipe_delete,
        name='delete'
    ),
    path(
        'recipes/add/',
        views.recipe_edit_or_create,
        name='add'
    ),
    path(
        'subscriptions/',
        views.SubscriptionView.as_view(),
        name='subscriptions',
    ),
    path(
        'shoplist/',
        views.cart,
        name='shoplist'
    ),
]
