from django.urls import path

from api.views import AddToFavorites, RemoveFromFavorite, AddToFollows

urlpatterns = [
    path('favorites/', AddToFavorites.as_view()),
    path('favorites/<int:id>/', RemoveFromFavorite.as_view()),
    path('subscriptions/', AddToFollows.as_view()),
    path('subscriptions/<int:author_id>/', AddToFollows.as_view()),
]
