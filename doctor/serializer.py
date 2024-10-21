from rest_framework import serializers
from .models import Doctor, DockterBranch


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['branch', 'address', 'state', 'picture',
                  'description', 'id_active', 'responsiveness', ]


class DockterBranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = DockterBranch
        fields = '__all__'
