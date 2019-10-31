from django.contrib.auth.models import User
from rest_framework import serializers
from .models import UserProfile, FriendNotification

from rest_framework.reverse import reverse
class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('pk', 'username', 'password', 'email')
        read_only_fields = ('pk',)

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
        )

        user.set_password(validated_data['password'])
        user.save()

        return user
class UserProfileFriendListSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['pk','public_key','profile_picture']

class UserFriendListSerializer(serializers.ModelSerializer):
    userprofile = UserProfileFriendListSerializer()
    class Meta:
        model = User
        fields = ['pk', 'username', 'email', 'userprofile']
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['pk', 'username', 'email']
class UserProfileListSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = UserProfile
        fields = ['user', 'public_key']

class FriendListSerializer(serializers.ModelSerializer):
    friends = UserFriendListSerializer(many=True)
    class Meta:
        model = UserProfile
        fields = ['friends']

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = UserProfile
        fields = ['user', 'public_key', 'private_key', 'salt', 'iv', 'profile_picture']

class CurrentUserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    friends = UserFriendListSerializer(many=True)
    class Meta:
        model = UserProfile
        fields = ['user', 'public_key', 'private_key', 'salt', 'iv', 'profile_picture', 'invite_code', 'friends']

class UserProfileListSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = UserProfile
        fields = ['user', 'public_key']


    def get_is_friends_with(self, obj):
        userprofile = self.context['request'].user.userprofile
        if userprofile.friends.filter(pk=obj.id).exists():
            return True
        else:
            return False
    class Meta:
        model = User
        fields = ['pk', 'username', 'email', 'userprofile', 'is_friends_with']


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['public_key', 'private_key', 'iv', 'salt']
    def update(self, instance, validated_data):
        instance.public_key = validated_data.get('public_key', instance.public_key)
        instance.private_key = validated_data.get('private_key', instance.private_key)
        instance.iv = validated_data.get('iv', instance.iv)
        instance.salt = validated_data.get('salt', instance.salt)
        instance.save()
        return instance

class UserPictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['profile_picture']
    def update(self, instance, validated_data):
        instance.profile_picture = validated_data.get('profile_picture', instance.profile_picture)
        instance.save()
        return instance



class FriendNotificationCreateSerializer(serializers.ModelSerializer):
    receiver = serializers.UUIDField()
    class Meta:
        model = FriendNotification
        fields = ['receiver']

    def create(self, validated_data):
        request = self.context.get('request')
        receiver=UserProfile.objects.get(invite_code=validated_data['receiver'])
        return FriendNotification.objects.create(sender=request.user.userprofile, receiver=receiver)

class FriendNotificationAcceptSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendNotification
        fields = ['pk']


class FriendNotificationListSerializer(serializers.ModelSerializer):
    accept_url = serializers.SerializerMethodField()
    decline_url = serializers.SerializerMethodField()
    sender = UserProfileListSerializer()

    class Meta:
        model = FriendNotification
        fields = ['sender', 'accept_url', 'decline_url']


    def get_accept_url(self, obj):
        return reverse('accept-friend', args=[obj.id], request=self.context['request'])

    def get_decline_url(self, obj):
        return reverse('decline-friend', args=[obj.id], request=self.context['request'])
