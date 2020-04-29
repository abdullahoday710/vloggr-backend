from rest_framework import serializers
from .models import Vlog, Segment, Album, Photo, UserCipher
from users.models import UserProfile
from django.contrib.auth.models import User
from django.utils import timezone
import json
from pyfcm import FCMNotification

push_service = FCMNotification(api_key="AAAAZTWbYVk:APA91bGMF7cH4DZwszkiMyysKIoh8rU55OiXr-F4_lQiWiBZ9_cNYFeuLQi87ApCDCF0SM2yBPFSJ6-ToNd1_8wJaWe2vPj90qz4oDF0IwJIuXBn6_k08JQJAC-2LnSLfyIEr77kTLk8")


class SegmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Segment
        fields = ['file']


class UserProfileShareWithSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    class Meta:
        model = UserProfile
        fields = ['username','pk', 'profile_picture', 'iv']

    def get_username(self, obj):
        return "{} {}".format(obj.first_name, obj.last_name)
class PhotoSerializer(serializers.ModelSerializer):
    cipher_object = serializers.JSONField
    shared_with = serializers.CharField(required=False)
    album = serializers.IntegerField(required=False)
    class Meta:
        model = Photo
        fields = ['cipher_object', 'shared_with', 'album', 'file', 'iv']

    def create(self, validated_data):
        photo = Photo.objects.create(
        cipher_object = validated_data['cipher_object'],
        file = validated_data['file'],
        iv = validated_data['iv'],
        user = self.context['request'].user.userprofile)
        if "album" in validated_data.keys():
            album = Album.objects.get(pk=validated_data['album'])
            photo.album = album

        if 'shared_with' in validated_data.keys():
            shared_with_data = json.loads(validated_data['shared_with'])
            users = UserProfile.objects.filter(pk__in=shared_with_data)
            # FCM notification title and body
            user = self.context['request'].user.userprofile
            username = "{} {}".format(user.first_name, user.last_name)
            message_title = username
            message_body = "has shared a picture with you"
            for userprofile in users:
                # TODO: check if the user we are sharing with is actually friends with the sender
                photo.shared_with.add(userprofile)
                #FCM PUSH NOTIFICATION
                registration_id = userprofile.fcm_token
                if registration_id:
                    push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)
        photo.save()
        return photo


class VlogSerializer(serializers.ModelSerializer):
    segments = SegmentSerializer(many=True, read_only=True)
    user_ciphers = serializers.CharField(required=True)
    shared_with = serializers.CharField(required=False)
    album = serializers.IntegerField(required=False)
    class Meta:
        model = Vlog
        fields = ['playlist', 'thumbnail', 'pk','segments','shared_with','user_ciphers','album']

    def create(self, validated_data):
        vlog = Vlog.objects.create(playlist=validated_data['playlist'], thumbnail=validated_data['thumbnail'], user=self.context['request'].user.userprofile)

        if "album" in validated_data.keys():
            album = Album.objects.get(pk=album_data)
            vlog.album = album

        if "shared_with" in validated_data.keys():
            shared_with_data = json.loads(validated_data["shared_with"])
            user_ciphers = json.loads(validated_data['user_ciphers'])

            # FCM notification title and body
            user = self.context['request'].user.userprofile
            shared_with_data.append(user.pk)
            users = UserProfile.objects.filter(pk__in=shared_with_data)
            username = "{} {}".format(user.first_name, user.last_name)
            message_title = username
            message_body = "has shared a vlog with you"
            for userprofile in users:
                for user_cipher in user_ciphers.items():
                    email = user_cipher[0]
                    cipher = user_cipher[1]
                    user_cipher_obj = UserCipher(email=email, cipher=cipher)
                    user_cipher_obj.save()
                    vlog.user_ciphers.add(user_cipher_obj)

                vlog.shared_with.add(userprofile)

                #FCM PUSH NOTIFICATION
                if userprofile != user:
                    registration_id = userprofile.fcm_token
                    if registration_id:
                        push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)

        # the request.FILES is temporary and will be used development only,
        # in production we will use amazon s3 urls instead
        segments_data = self.context.get('view').request.FILES
        for segment_data in segments_data.values():
            if segment_data.name.endswith(".ts"):
                Segment.objects.create(vlog=vlog, file=segment_data)
        vlog.save()
        return vlog

    def update(self, instance, validated_data):
        album = Album.objects.get(pk=validated_data['album'])
        instance.album = album
        instance.save()
        return instance.pk

class UserCipherSerializer(serializers.Serializer):
    email = serializers.CharField()
    cipher = serializers.CharField()
    class Meta:
        model = UserCipher
        fields = ['email', 'cipher']

class VlogListSerializer(serializers.ModelSerializer):
    user_ciphers = UserCipherSerializer(many=True)
    filename = serializers.SerializerMethodField()
    thumb_filename = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()
    year = serializers.SerializerMethodField()
    user = UserProfileShareWithSerializer(read_only=True)
    timestamp = serializers.DateTimeField()
    class Meta:
        model = Vlog
        fields = ['user','playlist', "thumbnail", 'user_ciphers', 'pk', 'filename', "thumb_filename", "type", 'timestamp', 'year']
    def get_type(self, obj):
        return "vlog"
    def get_filename(self, obj):
        return obj.playlist.name
    def get_thumb_filename(self, obj):
        return obj.thumbnail.name
    def get_year(self, obj):
        return obj.timestamp.year


class PhotoListSerializer(serializers.ModelSerializer):
    cipher_object = serializers.JSONField
    filename = serializers.SerializerMethodField()
    year = serializers.SerializerMethodField()
    user = UserProfileShareWithSerializer(read_only=True)
    timestamp = serializers.DateTimeField()
    type = serializers.SerializerMethodField()
    class Meta:
        model = Photo
        fields = ['user', 'cipher_object', 'pk', 'filename', 'timestamp', 'year', 'type', 'file', 'iv']
    def get_filename(self, obj):
        return obj.file.name
    def get_year(self, obj):
        return obj.timestamp.year
    def get_type(self, obj):
        return "photo"


class AlbumCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = ['name']

    def create(self,validated_data):
        album = Album.objects.create(user=self.context['request'].user.userprofile, name=validated_data['name'])
        album.save()
        return album
