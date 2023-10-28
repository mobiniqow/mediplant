from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from authenticate.permissions import AdminPermission, SuperAdminPermission, UserPermission
from logs.models import Logs
from .models import Country, City
from .serializers import CountrySerializer, CitySerializer


class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = [IsAdminUser]

    def check_permissions(self, request):
        if self.action in ['list', 'retrieve']:
            return
        super().check_permissions(request)

    def create(self, request, *args, **kwargs):
        # اینجا کد جدید را قرار دهید
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        bus = serializer.save()
        # اینجا کد جدید را قرار دهید

        Logs.objects.create(type=Logs.Type.CREATE,
                            content=f"   {request.user.first_name} {request.user.last_name}  کشور  با نام {bus.name} و ایدی {bus.id} ساخت ")
        return Response({'status': 'success', 'data': serializer.data})

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        Logs.objects.create(type=Logs.Type.UPDATE,
                            content=f"{request.user.first_name} {request.user.last_name}  کشور با نام {serializer.data['name']} و ایدی {instance.id} ویرایش کرد ")
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        id = instance.id
        self.perform_destroy(instance)
        Logs.objects.create(type=Logs.Type.DELETE,
                            content=f"{request.user.first_name} {request.user.last_name}  کشور با نام {instance.name} و ایدی {id} حذف کرد ")
        return Response(status=status.HTTP_204_NO_CONTENT)


class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = [IsAdminUser]

    def check_permissions(self, request):
        if self.action in ['list', 'retrieve']:
            return
        super().check_permissions(request)

    def create(self, request, *args, **kwargs):
        # اینجا کد جدید را قرار دهید
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        bus = serializer.save()
        # اینجا کد جدید را قرار دهید

        Logs.objects.create(type=Logs.Type.CREATE,
                            content=f"   {request.user.first_name} {request.user.last_name}  شهر  با نام {bus.name} و ایدی {bus.id} ساخت ")
        return Response({'status': 'success', 'data': serializer.data})

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        Logs.objects.create(type=Logs.Type.UPDATE,
                            content=f"{request.user.first_name} {request.user.last_name}  شهر با نام {serializer.data['name']} و ایدی {instance.id} ویرایش کرد ")
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        id = instance.id
        self.perform_destroy(instance)
        Logs.objects.create(type=Logs.Type.DELETE,
                            content=f"{request.user.first_name} {request.user.last_name}  شهر با نام {instance.name} و ایدی {id} حذف کرد ")
        return Response(status=status.HTTP_204_NO_CONTENT)
