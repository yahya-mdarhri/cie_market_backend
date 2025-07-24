from config import settings
from config.pagination import Paginator
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
from rest_framework.parsers import MultiPartParser, FormParser

from accounts.models import *
from .models import *
from .serializers import *

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

#this endpoint is used going to change depending on the what a user can see

# MEADIA_TYPE = ['application/x-www-form-urlencoded', 'application/json']

class ListAffiliationsView(viewsets.ViewSet):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Retrieve a list of all affiliations",
        manual_parameters=Paginator.PARAMETERS_DOCS,
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
        affiliations = Affiliation.objects.all().order_by('id')
        paginator = Paginator()
        results = paginator.paginate_queryset(affiliations, request)
        serializer = AffiliationSerializer(results, many=True, context={'request': request})
        return paginator.get_paginated_response(serializer.data)

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
            serializer = AffiliationSerializer(affiliation, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Affiliation.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

class ListInventorsView(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Retrieve a list of all inventors",
        manual_parameters=Paginator.PARAMETERS_DOCS,
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
        inventors = Inventor.objects.all().order_by('id')
        paginator = Paginator()
        results = paginator.paginate_queryset(inventors, request)
        serializer = InventorSerializer(results, many=True, context={'request': request})
        return paginator.get_paginated_response(serializer.data)

class GetInventorView(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

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
            serializer = InventorSerializer(inventor, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Inventor.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
          


class ListPatentsView(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Retrieve patents associated with the authenticated inventor",
        manual_parameters=Paginator.PARAMETERS_DOCS,
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
      patents = Patent.objects.filter(inventors=inventor).order_by('id')
      paginator = Paginator()
      results = paginator.paginate_queryset(patents, request)
      serializer = PatentSerializer(results, many=True, context={'request': request})
      return paginator.get_paginated_response(serializer.data)

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
            serializer = PatentSerializer(patent, context={'request': request})
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
        ] + Paginator.PARAMETERS_DOCS,
        tags=['Patents'],
    )
    def list(self, request, id=None):
        try:
            inventor = Inventor.objects.get(id=id)
            patents = Patent.objects.filter(inventors=inventor).order_by('id')
            paginator = Paginator()
            results = paginator.paginate_queryset(patents, request)
            serializer = PatentSerializer(results, many=True, context={'request': request})
            return paginator.get_paginated_response(serializer.data)
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
      ] + Paginator.PARAMETERS_DOCS,
      tags=['Patents'],
  )
  def list(self, request, id=None):
    try:
      affiliation = Affiliation.objects.get(id=id.upper())
      patents = Patent.objects.filter(affiliation=affiliation).order_by('id')
      paginator = Paginator()
      results = paginator.paginate_queryset(patents, request)
      serializer = PatentSerializer(results, many=True, context={'request': request})
      return paginator.get_paginated_response(serializer.data)
    except Affiliation.DoesNotExist:
      return Response(status=status.HTTP_404_NOT_FOUND)
    
class GetCoInventorsView(viewsets.ViewSet):
  permission_classes = [IsAuthenticated]

  @swagger_auto_schema(
      operation_description="Get the list of co-inventors for the patents associated with the current user.",
      manual_parameters=Paginator.PARAMETERS_DOCS,
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
      patents = Patent.objects.filter(inventors=inventor).order_by('id')
      co_inventors = set()
      for patent in patents:
        co_inventors.update(patent.inventors.exclude(id=inventor.id))
      paginator = Paginator()
      results = paginator.paginate_queryset(list(co_inventors), request)
      serializer = InventorSerializer(results, many=True, context={'request': request})
      return paginator.get_paginated_response(serializer.data)
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
      ] + Paginator.PARAMETERS_DOCS,
      tags=['Inventors'],
  )
  def list(self, request, id=None):
    try:
      inventor = Inventor.objects.get(id=id)
      patents = Patent.objects.filter(inventors=inventor).order_by('id')
      co_inventors = set()
      for patent in patents:
        co_inventors.update(patent.inventors.exclude(id=id))
      paginator = Paginator()
      results = paginator.paginate_queryset(list(co_inventors), request)
      serializer = InventorSerializer(results, many=True, context={'request': request})
      return paginator.get_paginated_response(serializer.data)
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
      ] + Paginator.PARAMETERS_DOCS,
      tags=['Patents'],
  )
  def list(self, request, inv_a=None, inv_b=None):
    try:
      inventor_a = Inventor.objects.get(id=inv_a)
      inventor_b = Inventor.objects.get(id=inv_b)
      patents = Patent.objects.filter(inventors=inventor_a).filter(inventors=inventor_b).order_by('id')
      paginator = Paginator()
      results = paginator.paginate_queryset(patents, request)
      serializer = PatentSerializer(results, many=True, context={'request': request})
      return paginator.get_paginated_response(serializer.data)
    except Inventor.DoesNotExist:
      return Response(status=status.HTTP_404_NOT_FOUND)
    

class ListTicketsView(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="list tickets associated with the authenticated inventor",
        manual_parameters=Paginator.PARAMETERS_DOCS,
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
      tickets = Ticket.objects.filter(inventors=inventor, is_draft=False).order_by('id')
      paginator = Paginator()
      results = paginator.paginate_queryset(tickets, request)
      serializer = TicketSerializer(results, many=True, context={'request': request})
      return paginator.get_paginated_response(serializer.data)

class ListDraftTicketsView(viewsets.ViewSet):
		permission_classes = [IsAuthenticated]

		@swagger_auto_schema(
				operation_description="list draft tickets associated with the authenticated inventor",
				manual_parameters=Paginator.PARAMETERS_DOCS,
				responses={
						200: openapi.Response(
								description="Authenticated User's draft tickets ",
								schema=TicketSerializer(many=True)
						),
						401: "Unauthorized"
				},
				tags=['Tickets'],
		)
		def list(self, request):
			user = request.user
			inventor = user.inventor
			paginator = Paginator()
			tickets = Ticket.objects.filter(inventors=inventor, is_draft=True).order_by('id')
			results = paginator.paginate_queryset(tickets, request)
			serializer = TicketSerializer(results, many=True, context={'request': request})
			return paginator.get_paginated_response(serializer.data)

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
            serializer = TicketSerializer(ticket, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Ticket.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
          
          
    @swagger_auto_schema(
        operation_description="Update a ticket by its ID",  
        request_body=TicketSerializer,
        responses={
            200: openapi.Response(
                description="Ticket updated successfully",
                schema=TicketSerializer()
            ),
            400: openapi.Response(
                description="Invalid data provided",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'error': openapi.Schema(type=openapi.TYPE_STRING),
                    }
                )
            ),
            401: "Unauthorized",
            403: "Forbidden"
        },
        tags=['Tickets'],
    )
    def update(self, request, id=None):
        try:
            ticket = Ticket.objects.get(id=id)
            if not ticket.inventors.filter(id=request.user.inventor.id).exists():
                return Response({"error": "You dont have access to this ticket"}, status=status.HTTP_403_FORBIDDEN)
            serializer = TicketSerializer(ticket, data=request.data, partial=True, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Ticket.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
          
    @swagger_auto_schema(
        operation_description="Delete a ticket by its ID",
        responses={
            204: openapi.Response("Ticket deleted successfully"),
            404: openapi.Response("Ticket not found"),
            403: openapi.Response("You dont have access to this ticket")
        },
        tags=['Tickets'],
    )
    def destroy(self, request, id=None):
        try:
            ticket = Ticket.objects.get(id=id)
            if not ticket.inventors.filter(id=request.user.inventor.id).exists():
                return Response({"error": "You dont have access to this ticket"}, status=status.HTTP_403_FORBIDDEN)
            ticket.delete()
            return Response({"message": "Ticket deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Ticket.DoesNotExist:
            return Response({"error": "Ticket not found"}, status=status.HTTP_404_NOT_FOUND)

class CreateTicketView(viewsets.ViewSet):
		permission_classes = [IsAuthenticated]

		@swagger_auto_schema(
				operation_description="Create a new ticket",
				request_body=TicketSerializer,
				responses={
						201: openapi.Response(
								description="Ticket created successfully",
								schema=TicketSerializer()
						),
						400: openapi.Response(
								description="Invalid data provided",
								schema=openapi.Schema(
										type=openapi.TYPE_OBJECT,
										properties={
												'error': openapi.Schema(type=openapi.TYPE_STRING),
										}
								)
						),
						401: "Unauthorized"
				},
				tags=['Tickets'],
		)
		def create(self, request):
				data = request.data.copy() 
				inventors = data.getlist('inventors') if hasattr(data, 'getlist') else data.get('inventors', [])
				if not inventors:
					inventors = [str(request.user.inventor.id)]
				elif str(request.user.inventor.id) not in inventors:
						inventors = list(set([str(i) for i in inventors] + [str(request.user.inventor.id)]))
				data.setlist('inventors', inventors) if hasattr(data, 'setlist') else data.update({'inventors': inventors})

				serializer = TicketSerializer(data=data, context={'request': request})
				if serializer.is_valid():
						ticket = serializer.save()
						ActivityLog.objects.create(
								user=request.user,
								action=f"You created a ticket",
								activity_type='create'
						)
						# Notify co-inventors that they have been added to the ticket, but not the creator
						for inventor in ticket.inventors.all():
								if hasattr(inventor, 'user') and inventor.user != request.user:
										Notification.objects.create(
												user=inventor.user,
												message=f"You have been added to a ticket by {request.user.inventor.preferred_name}."
										)
						return Response(serializer.data, status=status.HTTP_201_CREATED)
				return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SearchInventorByNameView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Search inventors by name (case-insensitive)",
        manual_parameters=Paginator.PARAMETERS_DOCS,
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['name'],
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING, description='Name or part of the name to search for')
            }
        ),
        responses={
            200: openapi.Response(
                description="List of matching inventors",
                schema=InventorSerializer(many=True)
            ),
            400: "Missing or invalid 'name' in request body",
            404: "No inventors found matching the name",
            401: "Unauthorized"
        },
        tags=['Inventors'],
    )
    def post(self, request):
        name_query = request.data.get('name', None)
        if not name_query:
            return Response({"error": "Missing 'name' in request body"}, status=status.HTTP_400_BAD_REQUEST)
        inventors = Inventor.objects.filter(preferred_name__icontains=name_query).order_by('id').exclude(id=request.user.inventor.id)
        paginator = Paginator()
        results = paginator.paginate_queryset(inventors, request)
        if not results:
            return Response({"message": "No inventors found matching the query"}, status=status.HTTP_404_NOT_FOUND)
        serializer = InventorSerializer(results, many=True, context={'request': request})
        return paginator.get_paginated_response(serializer.data)
