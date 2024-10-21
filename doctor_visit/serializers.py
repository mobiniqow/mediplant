from rest_framework import serializers
from .models import DoctorVisit, Prescription


class DoctorVisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorVisit
        fields = '__all__'


class PrescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prescription
        fields = '__all__'
