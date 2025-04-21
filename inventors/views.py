
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

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

#this endpoint is used going to change depending on the what a user can see

# MEADIA_TYPE = ['application/x-www-form-urlencoded', 'application/json']

class ListAffiliationsView(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Retrieve a list of all affiliations",
        responses={
            200: openapi.Response(
                description="Array of affiliations",
                schema=AffiliationSerializer(many=True)
            ),
            401: 'Unauthorized'
        },
        tags=['Affiliations'],
    )
    def list(self, request):
        affiliations = Affiliation.objects.all()
        serializer = AffiliationSerializer(affiliations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class GetAffiliationView(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Retrieve a specific affiliation by ID",
        manual_parameters=[
            openapi.Parameter(
                'id',
                openapi.IN_PATH,
                description="ID of the affiliation",
                type=openapi.TYPE_STRING, 
                required=True
            )
        ],
        responses={
            200: openapi.Response(
                description="Affiliation data",
                schema=AffiliationSerializer(many=True)
            ),
            404: "Affiliation not found",
            401: "Unauthorized"
        },
        tags=['Affiliations'],
    )
    def retrieve(self, request, id=None):
        try:
            affiliation = Affiliation.objects.get(id=id)
            serializer = AffiliationSerializer(affiliation)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Affiliation.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

class ListInventorsView(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Retrieve a list of all inventors",
        responses={
            200: openapi.Response(
                description="Array of Inventors",
                schema=InventorSerializer(many=True),
            ),
            401: "Unauthorized"
        },
        tags=['Inventors'],
    )
    def list(self, request):
        inventors = Inventor.objects.all()
        serializer = InventorSerializer(inventors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class GetInventorView(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Retrieve a specific inventor by ID",
        manual_parameters=[
            openapi.Parameter(
                'id',
                openapi.IN_PATH,
                description="ID of the inventor",
                type=openapi.TYPE_STRING,
                required=True
            )
        ],
        responses={
            200: openapi.Response(
                description="Inventor data",
                schema=InventorSerializer(),
            ),
            404: "Inventor not found",
            401: "Unauthorized"
        },
        tags=['Inventors'],
    )
    def retrieve(self, request, id=None):
        try: 
            inventor = Inventor.objects.get(id=id)
            serializer = InventorSerializer(inventor)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Inventor.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
          


class ListPatentsView(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Retrieve patents associated with the authenticated inventor",
        responses={
            200: openapi.Response(
                description="Authenticated User's patents ",
                schema=PatentSerializer(many=True)
            ),
            401: "Unauthorized"
        },
        tags=['Patents'],
    )
    def list(self, request):
      user = request.user
      inventor = user.inventor
      patents = Patent.objects.filter(inventors=inventor)
      serializer = PatentSerializer(patents, many=True)
      return Response(serializer.data, status=status.HTTP_200_OK)

class GetPatentView(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Retrieve a patent by its ID",
        manual_parameters=[
            openapi.Parameter(
                'id',
                openapi.IN_PATH,
                description="ID of the patent",
                type=openapi.TYPE_STRING,
                required=True,
            )
        ],
        responses={
            200: openapi.Response(
                description="Authenticated User's P data",
                schema=PatentSerializer()
            ),
            401: openapi.Response('Unauthorized'),
            404: openapi.Response(description="Patent not found")
        },
        tags=['Patents'],
    )
    def retrieve(self, request, id=None):
        try:
            patent = Patent.objects.get(id=id)
            serializer = PatentSerializer(patent)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Inventor.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

class GetInventorPatentsView(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Get the list of patents for a specific inventor by their ID.",
        responses={
            200: PatentSerializer(many=True),
            404: openapi.Response('Inventor not found'),
            401: openapi.Response('Unauthorized')
        },
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_PATH, description="ID of the inventor", type=openapi.TYPE_STRING)
        ],
        tags=['Patents'],
    )
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

  @swagger_auto_schema(
      operation_description="Get the list of patents for a specific affiliation by its ID.",
      responses={
          200: PatentSerializer(many=True),
          404: openapi.Response('Affiliation not found'),
          401: openapi.Response('Unauthorized')
      },
      manual_parameters=[
          openapi.Parameter('id', openapi.IN_PATH, description="ID of the affiliation", type=openapi.TYPE_STRING)
      ],
      tags=['Patents'],
  )
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

  @swagger_auto_schema(
      operation_description="Get the list of co-inventors for the patents associated with the current user.",
      responses={
          200: InventorSerializer(many=True),
          404: openapi.Response('Inventor not found'),
          401: openapi.Response('Unauthorized')
      },
      tags=['Inventors'],
  )
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

  @swagger_auto_schema(
      operation_description="Get the list of co-inventors of a specific inventor by their ID.",
      responses={
          200: InventorSerializer(many=True),
          404: openapi.Response('Inventor not found'),
          401: openapi.Response('Unauthorized')
      },
      manual_parameters=[
          openapi.Parameter('id', openapi.IN_PATH, description="ID of the inventor", type=openapi.TYPE_STRING)
      ],
      tags=['Inventors'],
  )
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
    


class GetSharedPatentsView(viewsets.ViewSet):
  permission_classes = [IsAuthenticated]

  @swagger_auto_schema(
      operation_description="Get the list of patents shared between two inventors identified by their IDs.",
      responses={
          200: PatentSerializer(many=True),
          404: openapi.Response('Inventor not found'),
          401: openapi.Response('Unauthorized')
      },
      manual_parameters=[
          openapi.Parameter('inv_a', openapi.IN_PATH, description="ID of the first inventor", type=openapi.TYPE_STRING),
          openapi.Parameter('inv_b', openapi.IN_PATH, description="ID of the second inventor", type=openapi.TYPE_STRING)
      ],
      tags=['Patents'],
  )
  def list(self, request, inv_a=None, inv_b=None):
    try:
      inventor_a = Inventor.objects.get(id=inv_a)
      inventor_b = Inventor.objects.get(id=inv_b)
      patents = Patent.objects.filter(inventors=inventor_a).filter(inventors=inventor_b)
      serializer = PatentSerializer(patents, many=True)
      return Response(serializer.data, status=status.HTTP_200_OK)
    except Inventor.DoesNotExist:
      return Response(status=status.HTTP_404_NOT_FOUND)
    

class ListTicketsView(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="list tickets associated with the authenticated inventor",
        responses={
            200: openapi.Response(
                description="Authenticated User's tickets ",
                schema=TicketSerializer(many=True)
            ),
            401: "Unauthorized"
        },
        tags=['Tickets'],
    )
    def list(self, request):
      user = request.user
      inventor = user.inventor
      tickets = Ticket.objects.filter(inventors=inventor)
      serializer = TicketSerializer(tickets, many=True)
      return Response(serializer.data, status=status.HTTP_200_OK)

class GetTicketView(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Retrieve a ticket by its ID",
        manual_parameters=[
            openapi.Parameter(
                'id',
                openapi.IN_PATH,
                description="ID of the ticket",
                type=openapi.TYPE_STRING,
                required=True,
            )
        ],
        responses={
            200: openapi.Response(
                description="ticket data",
                schema=TicketSerializer()
            ),
            401: openapi.Response('Unauthorized'),
            403: openapi.Response("Has no access to this ticket", schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'error': openapi.Schema(type=openapi.TYPE_STRING),
                }
            )),
            404: openapi.Response(description="Ticket not found")
        },
        tags=['Tickets'],
    )
    def retrieve(self, request, id=None):
        try:
            ticket = Ticket.objects.get(id=id)
            if not ticket.inventors.filter(id=request.user.inventor.id).exists():
              return Response({"error": "You dont have access to this ticket"},status=status.HTTP_403_FORBIDDEN)
            serializer = TicketSerializer(ticket)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Inventor.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
