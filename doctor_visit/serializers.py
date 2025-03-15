from rest_framework import serializers
from .models import DoctorVisit, Prescription, DoctorVisitChat


class DoctorVisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorVisit
        fields = '__all__'


class PrescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prescription
        fields = '__all__'


class DoctorVisitChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorVisitChat
        fields = ['id', 'doctor_id', 'is_doctor', 'content', 'media']


class UserChatRequest(serializers.ModelSerializer):
    class Meta:
        model = DoctorVisitChat
        fields = ['is_doctor', 'content', 'media', 'doctor_id']

    def create(self, validated_data):
        validated_data['is_doctor'] = self.context.get('is_doctor')
        visit_id = self.context.get('doctor_id')
        print(validated_data)
        print(validated_data)
        if visit_id:
            visit = DoctorVisit.objects.get(pk=visit_id)
            validated_data['doctor_id'] = visit.doctor.id

        return super().create(validated_data)
