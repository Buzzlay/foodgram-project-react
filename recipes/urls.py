from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('favorites', views.FavoriteView.as_view(), name='favorites'),
    path('profiles/<str:username>', views.ProfileView.as_view(), name='profile'),
    path('recipes/<int:id>', views.RecipeDetailView.as_view(), name='recipe')
]
