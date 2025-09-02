from django.urls import path

from faedoguerra_app.auth import views

urlpatterns = [
    path('login/', views.auth_login),
]
