from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    TicketListCreateView, TicketDetailView,
    MessageCreateView, TicketAssignView,
    UserTicketsView, AdminTicketListView, TicketSectionViewSet
)
router = DefaultRouter()
router.register(r'ticket-sections', TicketSectionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('tickets/', TicketListCreateView.as_view(), name='ticket-list-create'),
    path('tickets/<int:pk>/', TicketDetailView.as_view(), name='ticket-detail'),
    path('tickets/<int:ticket_id>/messages/', MessageCreateView.as_view(), name='ticket-messages'),
    path('tickets/<int:pk>/assign/', TicketAssignView.as_view(), name='ticket-assign'),
    path('my-tickets/', UserTicketsView.as_view(), name='user-tickets'),
    path('admin/tickets/', AdminTicketListView.as_view(), name='admin-ticket-list'),
]
