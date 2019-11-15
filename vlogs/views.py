from django.shortcuts import render
from rest_framework.generics import CreateAPIView, ListAPIView,UpdateAPIView
from .serializers import VlogSerializer, VlogListSerializer, AlbumCreateSerializer
from rest_framework.permissions import AllowAny
from .models import Vlog
from rest_framework.response import Response
from rest_framework import status


class CreateVlogView(CreateAPIView):
    serializer_class = VlogSerializer
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({'info': 'sucess'}, status=status.HTTP_201_CREATED)

class UpdateVlogView(UpdateAPIView):
    serializer_class = VlogSerializer
    queryset = Vlog.objects.all()
class ListVlogView(ListAPIView):
    serializer_class = VlogListSerializer

    def get_queryset(self):
        user = self.request.user
        return Vlog.objects.filter(user=user.userprofile)

class ListSharedWithVlogView(ListAPIView):

    #permission_classes = [AllowAny]
    serializer_class = VlogListSerializer

    def get_queryset(self):
        user = self.request.user
        return Vlog.objects.filter(shared_with=user.userprofile)
        #return Vlog.objects.all()

class CreateAlbumView(CreateAPIView):
    serializer_class = AlbumCreateSerializer
