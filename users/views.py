import uuid

from django.shortcuts import render
from rest_framework.generics import (RetrieveAPIView,
CreateAPIView,
UpdateAPIView,
DestroyAPIView,
ListAPIView,
GenericAPIView,
)
from rest_framework.mixins import UpdateModelMixin
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
FriendListSerializer,
UserPictureSerializer,
CurrentUserProfileSerializer,
UpdateFcmTokenSerializer,
)
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, filters
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from .permissions import IsOwnerOrReadOnly


class UserProfileRetrieveView(RetrieveAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class UserCreateView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserCreateSerializer


class UserProfileUpdateView(UpdateAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileUpdateSerializer


class UpdateFcmTokenView(GenericAPIView, UpdateModelMixin):
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = UpdateFcmTokenSerializer
    def get_object(self):
        user = self.request.user.userprofile
        return UserProfile.objects.get(pk=user.pk)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class ChangeProfilePicture(UpdateAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    queryset = UserProfile.objects.all()
    serializer_class = UserPictureSerializer


class CurrentUserView(APIView):
    def get(self, request):
        serializer = CurrentUserProfileSerializer(request.user.userprofile)
        return Response(serializer.data)


class FriendListView(ListAPIView):
    serializer_class = FriendListSerializer
    def get_queryset(self):
        user = self.request.user.userprofile
        return UserProfile.objects.filter(pk=user.pk)


class CreateFriendRequestView(CreateAPIView):
    serializer_class = FriendNotificationCreateSerializer
    def create(self, request, *args, **kwargs):
        # checking if a FriendNotification object exist with the current sender/receiver
        receiver = get_object_or_404(UserProfile,invite_code=request.data['receiver'])

        if FriendNotification.objects.filter(sender=request.user.userprofile, receiver=receiver).exists():
            return Response({"info": "You already sent friend request to this person","profile_pic":receiver.profile_picture.url,"username":receiver.user.username}, status=403)
            # checking if the users are "friends"
        elif request.user.userprofile.friends.filter(pk=receiver.pk).exists():
            return Response({"info": "You are already friends with this person","profile_pic":receiver.profile_picture.url,"username":receiver.user.username}, status=403)
        elif request.data['receiver'] == str(request.user.userprofile.invite_code):
            return Response({"info": "You are not allowed to send friend requests to yourself.","profile_pic":receiver.profile_picture.url,"username":receiver.user.username}, status=403)

        else:
            # creating the friend request
            super(CreateFriendRequestView, self).create(request, *args, **kwargs)
            # updating the receiver invite code because the old one is used.
            receiver.invite_code = uuid.uuid4()
            receiver.save()
            response = Response({"info":"sent","profile_pic":receiver.profile_picture.url,"username":receiver.user.username})
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
