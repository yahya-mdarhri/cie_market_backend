
from django.urls import path, include
from rest_framework import routers
from .views import *

app_name = 'inventors'

router = routers.SimpleRouter()
router.register(r'patents', ListPatentsView, basename='patents')
router.register(r'inventors', ListInventorsView, basename='inventors')
router.register(r'affiliations', ListAffiliationsView, basename='affiliations')

urlpatterns = [
    path('', include(router.urls)),
    path('patent/<int:id>/', GetPatentView.as_view({'get': 'list'}), name='patent-detail'),
    path('inventor/<str:id>/', GetInventorsView.as_view({'get': 'list'}), name='inventor-detail'),
    path('affiliation/<str:id>/', GetAffiliationView.as_view({'get': 'list'}), name='affiliation-detail'),
]
# email=a@email.com&password=hamza