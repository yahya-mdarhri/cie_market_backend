
from rest_framework.views import APIView
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
)
from rest_framework import (
    status,
    viewsets
)
from rest_framework.response import Response
from rest_framework import status

from .models import *
from .serializers import *


#this endpoint is used going to change depending on the what a user can see

class ListAffiliationsView(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        affiliations = Affiliation.objects.all()
        serializer = AffiliationSerializer(affiliations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class GetAffiliationView(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request, id=None):
        try:
            affiliation = Affiliation.objects.get(id=id)
            serializer = AffiliationSerializer(affiliation)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Affiliation.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

class ListInventorsView(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        inventors = Inventor.objects.all()
        serializer = InventorSerializer(inventors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class GetInventorsView(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request, id=None):
        try: 
            affiliation = Inventor.objects.get(id=id)
            serializer = InventorSerializer(affiliation)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Inventor.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
          


class ListPatentsView(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
      user = request.user
      inventor = user.inventor
      patents = Patent.objects.filter(inventors=inventor)
      serializer = PatentSerializer(patents, many=True)
      return Response(serializer.data, status=status.HTTP_200_OK)

class GetPatentView(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request, id=None):
        try:
            patent = Patent.objects.get(id=id)
            serializer = PatentSerializer(patent)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Inventor.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

class GetInventorPatentsView(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request, id=None):
        try:
            inventor = Inventor.objects.get(id=id)
            patents = Patent.objects.filter(inventors=inventor)
            serializer = PatentSerializer(patents, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Inventor.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

class GetAffiliationPatentsView(viewsets.ViewSet):
  permission_classes = [IsAuthenticated]

  def list(self, request, id=None):
    try:
      affiliation = Affiliation.objects.get(id=id.upper())
      patents = Patent.objects.filter(affiliation=affiliation)
      serializer = PatentSerializer(patents, many=True)
      return Response(serializer.data, status=status.HTTP_200_OK)
    except Affiliation.DoesNotExist:
      return Response(status=status.HTTP_404_NOT_FOUND)
    
class GetCoInventorsView(viewsets.ViewSet):
  permission_classes = [IsAuthenticated]

  def list(self, request):
    user = request.user
    try:
      inventor = user.inventor
      patents = Patent.objects.filter(inventors=inventor)
      co_inventors = set()
      for patent in patents:
        co_inventors.update(patent.inventors.exclude(id=inventor.id))
      serializer = InventorSerializer(co_inventors, many=True)
      return Response(serializer.data, status=status.HTTP_200_OK)
    except Inventor.DoesNotExist:
      return Response(status=status.HTTP_404_NOT_FOUND)

class GetInventorCoInventorsView(viewsets.ViewSet):
  permission_classes = [IsAuthenticated]

  def list(self, request, id=None):
    try:
      inventor = Inventor.objects.get(id=id)
      patents = Patent.objects.filter(inventors=inventor)
      co_inventors = set()
      for patent in patents:
        co_inventors.update(patent.inventors.exclude(id=id))
      serializer = InventorSerializer(co_inventors, many=True)
      return Response(serializer.data, status=status.HTTP_200_OK)
    except Inventor.DoesNotExist:
      return Response(status=status.HTTP_404_NOT_FOUND)