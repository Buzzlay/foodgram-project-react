from django.urls import path

from .views import IndexView, FavoriteView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('favorites', FavoriteView.as_view(), name='favorites')
]
