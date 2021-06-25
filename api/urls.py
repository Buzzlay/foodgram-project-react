from django.urls import path

from api.views import AddToFavorites, AddToFollows, Purchases, IngredientView

urlpatterns = [
    path('favorites/', AddToFavorites.as_view()),
    path('favorites/<int:id>/', AddToFavorites.as_view()),
    path('ingredients', IngredientView.as_view(), name='ingredients'),
    path('subscriptions/', AddToFollows.as_view()),
    path('subscriptions/<int:author_id>/', AddToFollows.as_view()),
    path('purchases/', Purchases.as_view()),
    path('purchases/<int:recipe_id>/', Purchases.as_view()),
]