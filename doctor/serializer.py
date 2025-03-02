from rest_framework import serializers
from .models import Doctor, DockterBranch


class DoctorSerializer(serializers.ModelSerializer):
    branch_name = serializers.CharField(source='branch.name', read_only=True)

    class Meta:
        model = Doctor
        fields = [
            'id', 'user', 'branch', 'branch_name', 'address', 'state',
            'picture', 'description', 'id_active', 'register_time',
            'responsiveness', 'postal_code', 'shaba'
        ]

class DockterBranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = DockterBranch
        fields = '__all__'
