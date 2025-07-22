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
    path('me/', UserMeView.as_view({'get': 'retrieve', 'put': 'update'}), name='me'),

    path('login/', LoginView.as_view({'post':'create'}), name='login'),
    path('register/', RegisterView.as_view({'post':'create'}), name='register'),
    path('logout/', LogoutView.as_view({'get':'retrieve'}), name='logout'),

    path('create-account/', ManagerCreateInventorAccount.as_view({'post': 'create'}), name='create-account'),

    path('change-password/', ChangePasswordView.as_view({'post': 'create'}), name='change-password'),
    path('reset-password/', ResetPasswordView.as_view({'post': 'create'}), name='reset-password'),  # <-- added
    path('reset-password-confirm/<uidb64>/<token>/', ResetPasswordConfirmView.as_view({'post': 'create'}), name='reset-password-confirm'),

		path('activity-logs/', ActivityLogs.as_view({'get': 'list'}), name='activity-logs'),
		path('notifications/', NotificationsList.as_view({'get': 'list'}), name='notifications-list'),
		path('activity-logs/<int:id>/', ActivityLogDetails.as_view({'get': 'retrieve'}), name='activity-log-detail'),
		path('notifications/<int:id>/', NotificationDetails.as_view({'get': 'retrieve', 'put': 'mark_as_read', 'delete': 'destroy'}), name='notification-detail'),
]