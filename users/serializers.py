from .models import User
from rest_framework import serializers
from .models import UserProfile, FriendNotification

from rest_framework.reverse import reverse
class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('pk', 'password', 'email')
        read_only_fields = ('pk',)

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
        )

        user.set_password(validated_data['password'])
        user.save()
        # setting this to none so it doesn't get returned with the user instance
        user.password = None
        return user
class UserProfileFriendListSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    class Meta:
        model = UserProfile
        fields = ['pk','public_key','profile_picture', 'username']

    def get_username(self, obj):
        return "{} {}".format(obj.first_name, obj.last_name)
class UserFriendListSerializer(serializers.ModelSerializer):
    userprofile = UserProfileFriendListSerializer()
    class Meta:
        model = User
        fields = ['pk', 'email', 'userprofile']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['pk', 'email']

class UserProfileListSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = UserProfile
        fields = ['user', 'public_key', 'profile_picture']

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
    friends = UserFriendListSerializer(many=True)
    username = serializers.SerializerMethodField()
    user = UserSerializer()
    class Meta:
        model = UserProfile
        fields = ['public_key', 'private_key', 'salt', 'iv', 'profile_picture', 'invite_code', 'friends', 'username', 'user']

    def get_username(self, obj):
        return "{} {}".format(obj.first_name, obj.last_name)

class UserProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['public_key', 'private_key', 'iv', 'salt', 'first_name', 'last_name']
    def update(self, instance, validated_data):
        instance.public_key = validated_data.get('public_key', instance.public_key)
        instance.private_key = validated_data.get('private_key', instance.private_key)
        instance.iv = validated_data.get('iv', instance.iv)
        instance.salt = validated_data.get('salt', instance.salt)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
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
    username = serializers.SerializerMethodField()
    class Meta:
        model = FriendNotification
        fields = ['sender', 'accept_url', 'decline_url', 'username']

    def get_username(self, obj):
        return "{} {}".format(obj.sender.first_name, obj.sender.last_name)

    def get_accept_url(self, obj):
        return reverse('accept-friend', args=[obj.id], request=self.context['request'])

    def get_decline_url(self, obj):
        return reverse('decline-friend', args=[obj.id], request=self.context['request'])


class UpdateFcmTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['fcm_token']
