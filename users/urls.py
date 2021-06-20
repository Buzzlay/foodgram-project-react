from django.urls import path

from . import views

urlpatterns = [
    path('registration/',
         views.Registration.as_view(),
         name='registration'),
]
