from django.urls import path
from .views import DoctorListByBranch, DockterBranchListView

urlpatterns = [
    path('api/doctors/<int:branch_id>/', DoctorListByBranch.as_view(), name='doctor_list_by_branch'),
    path('dockter-branches/', DockterBranchListView.as_view(), name='dockter-branch-list'),
]
