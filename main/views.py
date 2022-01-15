from django.shortcuts import render
from django.views import generic
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from main.models import Airplane, Person, Ticket, Country
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


class TicketDetailView(generics.RetrieveAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer


class TicketUpdateView(generics.UpdateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer


class TicketDeleteView(generics.DestroyAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer


class TicketView(generics.ListCreateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

    def get_serializer_context(self):
        return {'request': self.request}