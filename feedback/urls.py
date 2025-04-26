from django.urls import path
from .views import (
    get_feedback_products,
    submit_feedback,
    finalize_feedback,
    get_approved_feedbacks,
)

urlpatterns = [
    path('<slug:slug>/products/', get_feedback_products, name='get_feedback_products'),
    path('<slug:slug>/submit/<int:product_id>/', submit_feedback, name='submit_feedback'),
    path('<slug:slug>/finalize/', finalize_feedback, name='finalize_feedback'),
    path('shop/<int:shop_id>/feedbacks/<int:product_id>', get_approved_feedbacks, name='get_approved_feedbacks'),
]
