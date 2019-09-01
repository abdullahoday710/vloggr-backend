from django.shortcuts import render
from rest_framework.generics import CreateAPIView, ListAPIView
from .serializers import VlogSerializer, VlogListSerializer
from rest_framework.permissions import AllowAny
from .models import Vlog
# Create your views here.

class CreateVlogView(CreateAPIView):
    #permission_classes = [AllowAny]
    serializer_class = VlogSerializer




class ListVlogView(ListAPIView):

    permission_classes = [AllowAny]
    serializer_class = VlogListSerializer

    def get_queryset(self):
        user = self.request.user
        return Vlog.objects.filter(user=user.userprofile)
        #return Vlog.objects.all()
