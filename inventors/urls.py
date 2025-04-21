
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
    path('patents/', ListPatentsView.as_view({'get': 'list'}), name='pmy-patents'),
    path('patent/<int:id>/', GetPatentView.as_view({'get': 'retrieve'}), name='patent-detail'),
    path ('patents/<str:inv_a>/<str:inv_b>', GetSharedPatentsView.as_view({'get': 'list'}), name='shared-patents'),
    
    path('tickets/', ListTicketsView.as_view({'get': 'list'}), name='my-tickets'),
    path('ticket/<int:id>/', GetTicketView.as_view({'get': 'retrieve'}), name='ticket-detail'),
    
    path('inventor/co-inventors', GetCoInventorsView.as_view({'get': 'list'}), name='my-coInventors'),
    path('inventor/<str:id>/', GetInventorView.as_view({'get': 'retrieve'}), name='inventor-detail'),
    path('inventor/<str:id>/patents', GetInventorPatentsView.as_view({'get': 'list'}), name='inventor-patents'),
    path('inventor/<str:id>/co-inventors', GetInventorCoInventorsView.as_view({'get': 'list'}), name='inventor-co_inventors'),

    path('affiliation/<str:id>/', GetAffiliationView.as_view({'get': 'retrieve'}), name='affiliation-detail'),
    path('affiliation/<str:id>/patents', GetAffiliationPatentsView.as_view({'get': 'list'}), name='affiliation-detail'),
]
# email=a@email.com&password=hamza