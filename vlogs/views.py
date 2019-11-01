from django.shortcuts import render
from rest_framework.generics import CreateAPIView, ListAPIView
from .serializers import VlogSerializer, VlogListSerializer
from rest_framework.permissions import AllowAny
from .models import Vlog
from rest_framework.response import Response
from rest_framework import status
# Create your views here.

class CreateVlogView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = VlogSerializer
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({'info': 'sucess'}, status=status.HTTP_201_CREATED)

class ListVlogView(ListAPIView):

    #permission_classes = [AllowAny]
    serializer_class = VlogListSerializer

    def get_queryset(self):
        user = self.request.user
        return Vlog.objects.filter(user=user.userprofile)
        #return Vlog.objects.all()

class ListSharedWithVlogView(ListAPIView):

    #permission_classes = [AllowAny]
    serializer_class = VlogListSerializer

    def get_queryset(self):
        user = self.request.user
        return Vlog.objects.filter(shared_with=user.userprofile)
        #return Vlog.objects.all()
