from django.urls import path, include

from rest_framework.urlpatterns import format_suffix_patterns

from . import views


urlpatterns = [
    path(
        '',
        views.IndexView.as_view(),
        name='index'
    ),
    path(
        '<slug:tag_slug>',
        views.recipes_by_tag,
        name='recipes_list_by_tag'
    ),
    path('api/', include('api.urls')),
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
        'subscriptions/',
        views.SubscriptionView.as_view(),
        name='subscriptions',
    ),
    path(
        'shoplist/',
        views.cart,
        name='shoplist'
    )
]
