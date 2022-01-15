from django.urls import path

from main.views import TicketView, TicketDetailView, TicketUpdateView, TicketDeleteView

urlpatterns = [
    path('ticket/', TicketView.as_view()),
    path('ticket/<int:pk>', TicketDetailView.as_view()),
    path('ticket-update/<int:pk>', TicketUpdateView.as_view()),
    path('ticket-delete/<int:pk>', TicketDeleteView.as_view()),



]