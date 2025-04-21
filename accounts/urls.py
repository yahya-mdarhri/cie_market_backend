
from django.urls import path, include
from rest_framework import routers
from .views import *


app_name = 'accounts'

# router = routers.SimpleRouter()
# router.register(r'home', HomeView, basename='home')
# router.register(r'login', LoginView, basename='login')
# router.register(r'logout', LogoutView, basename='logout')
# router.register(r'register', RegisterView, basename='register')

urlpatterns = [
    # path('', include(router.urls)),
    path('login/', LoginView.as_view({'post':'create'}), name='login'),
    path('register/', RegisterView.as_view({'post':'create'}), name='register'),
    path('logout/', LogoutView.as_view({'get':'retrieve'}), name='logout'),
]