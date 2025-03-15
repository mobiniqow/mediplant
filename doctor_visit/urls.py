from django.urls import path
from .views import RequestToDoctor, DoctorVisitChatListView, UserSendToDoctorMessage

urlpatterns = [
    path('request/<int:doctor_id>/', RequestToDoctor.as_view()),
    path('doctor-visit/<int:doctor_visit_id>/chats/', DoctorVisitChatListView.as_view(), name='doctor-visit-chats'),
    path('doctor-visit/<int:doctor_visit_id>/send-message/', UserSendToDoctorMessage.as_view(), name='doctor-visit-chats'),
]
