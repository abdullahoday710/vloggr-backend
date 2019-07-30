from django.shortcuts import render
from rest_framework.generics import (RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView, ListAPIView)
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .models import UserProfile, FriendNotification
from .serializers import (UserProfileSerializer,
 UserCreateSerializer,
 UserProfileUpdateSerializer,
 FriendNotificationCreateSerializer,
 FriendNotificationAcceptSerializer,
 FriendNotificationListSerializer,
 UserProfileListSerializer,
 UserSearchSerializer,
 )


from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, filters
from django.contrib.auth.models import User


from .serializers import FileSerializer

# Create your views here.
class UserProfileRetrieveView(RetrieveAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

class UserCreateView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserCreateSerializer

class UserProfileUpdateView(UpdateAPIView):
    # TODO: add owner or read only permission later
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileUpdateSerializer

class CurrentUserView(APIView):
    def get(self, request):
        serializer = UserProfileSerializer(request.user.userprofile)
        return Response(serializer.data)




class CreateFriendRequestView(CreateAPIView):
    serializer_class = FriendNotificationCreateSerializer
    def create(self, request, *args, **kwargs):
        # checking if a FriendNotification object exist with the current sender/receiver
        if FriendNotification.objects.filter(sender=request.user.userprofile, receiver=request.data['receiver']).exists():
            return Response({"info": "You are already sent friend request to this person"}, status=403)
        # checking if the users are "friends"
        elif request.user.userprofile.friends.filter(pk=request.data['receiver']).exists():
            return Response({"info": "You are already friends with this person"}, status=403)
        else:
            response = super(CreateFriendRequestView, self).create(request, *args, **kwargs)
            return response

class AcceptFriendRequestView(UpdateAPIView):
    queryset = FriendNotification.objects.all()

    serializer_class = FriendNotificationAcceptSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user.userprofile != instance.sender:
            if request.user.userprofile == instance.receiver:
                # adding friends here
                instance.receiver.friends.add(instance.sender.user)
                instance.sender.friends.add(instance.receiver.user)
                # deleting the notification here
                instance.delete()
                return Response({"info": "sucess"})
        else:
            return Response({"info": "bad request"}, status=400)


class DeclineFriendRequestView(DestroyAPIView):
    queryset = FriendNotification.objects.all()
    serializer_class = FriendNotificationAcceptSerializer




class FriendNotificationListView(ListAPIView):
    serializer_class = FriendNotificationListSerializer
    def get_queryset(self):
        user = self.request.user.userprofile
        return FriendNotification.objects.filter(receiver=user)



class UserSearchView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSearchSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'email']
class FileUploadView(APIView):
    permission_classes = [AllowAny]
    parser_class = (FileUploadParser,)

    methods = ['POST']

    def post(self, request, *args, **kwargs):

      file_serializer = FileSerializer(data=request.data)

      if file_serializer.is_valid():
          file_serializer.save()
          return Response(file_serializer.data, status=status.HTTP_201_CREATED)
      else:
          return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
