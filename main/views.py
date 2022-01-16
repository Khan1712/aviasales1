from django.db.models import Q
from django.shortcuts import render
from django.views import generic
from rest_framework import generics, viewsets, status
from rest_framework.decorators import api_view, action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from main.models import Airplane, Person, Ticket, Country
from main.permissions import IsAuthor
from main.serializers import AirplaneSerializer, PersonSerializer, TicketSerializer, CountrySerializer


# @api_view(['GET'])
# def airplane(request):
#     airplane = Airplane.objects.all()
#     serializer = AirplaneSerializer(airplane, many=True)
#     return Response(serializer.data)
#
#
# class PersonListView(APIView):
#     def get(self, request):
#         person = Person.objects.all()
#         serializer = PersonSerializer(person, many=True)
#         return Response(serializer.data)
#
#
# @api_view(['GET'])
# def ticket(request):
#     ticket = Ticket.objects.all()
#     serializer = TicketSerializer(ticket, many=True)
#     return Response(serializer.data)

#
# class CountryListView(APIView):
#     def get(self, request):
#         country = Country.objects.all()
#         serializer = CountrySerializer(country, many=True)
#         return Response(serializer.data)


# class TicketDetailView(generics.RetrieveAPIView):
#     queryset = Ticket.objects.all()
#     serializer_class = TicketSerializer
#
#
# class TicketUpdateView(generics.UpdateAPIView):
#     queryset = Ticket.objects.all()
#     serializer_class = TicketSerializer
#
#
# class TicketDeleteView(generics.DestroyAPIView):
#     queryset = Ticket.objects.all()
#     serializer_class = TicketSerializer


# class TicketView(generics.ListCreateAPIView):
#     queryset = Ticket.objects.all()
#     serializer_class = TicketSerializer


class AirplaneListView(generics.ListAPIView):
    queryset = Airplane.objects.all()
    serializer_class = AirplaneSerializer


class CountryListView(generics.ListAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class PersonListView(generics.ListAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]

    # def get_permissions(self):
    #     if self.action in ['create', 'update', 'partial_update', 'destroy']:
    #         permissions = [IsAuthor]
    #     else:
    #         permissions = [IsAuthenticated]
    #     return [permission() for permission in permissions]

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return []
        elif self.action == 'reviews':
            if self.request.method == 'POST':
                return [IsAuthenticated()]
            return []
        return [IsAdminUser()]

    @action(detail=False, methods=['get'])
    def own(self, request, pk=None):
        queryset = self.get_queryset()
        queryset = queryset.filter(author=request.user)
        serializer = TicketSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False)
    def search(self, request, pk=None):
        q = request.query_params.get('q')
        queryset = self.get_queryset()
        queryset = queryset.filter(Q(departure_time__icontains=q) |
                                   Q(ticket_price__icontains=q))
        serializer = TicketSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_serializer_context(self):
        return {'request': self.request}