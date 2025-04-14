
from django.urls import path, include
from rest_framework import routers
from .views import *


app_name = 'accounts'

router = routers.SimpleRouter()
router.register(r'home', HomeView, basename='home')
router.register(r'login', LoginView, basename='login')
router.register(r'logout', LogoutView, basename='logout')
router.register(r'register', RegisterView, basename='register')

urlpatterns = [
    path('', include(router.urls)),
]