from rest_framework import serializers
from .models import Vlog,Segment
from users.models import UserProfile
from django.contrib.auth.models import User
import json
from pyfcm import FCMNotification
push_service = FCMNotification(api_key="AAAAZTWbYVk:APA91bGMF7cH4DZwszkiMyysKIoh8rU55OiXr-F4_lQiWiBZ9_cNYFeuLQi87ApCDCF0SM2yBPFSJ6-ToNd1_8wJaWe2vPj90qz4oDF0IwJIuXBn6_k08JQJAC-2LnSLfyIEr77kTLk8")
class JSONSerializerField(serializers.Field):

    def to_representation(self, obj):
        try:
            return json.loads(obj)
        except (ValueError, Exception) as e:
            # log exception
            return obj

    def to_internal_value(self, data):
        return data

class SegmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Segment
        fields = ['file']
class userShareWithSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']
class UserProfileShareWithSerializer(serializers.ModelSerializer):
    user = userShareWithSerializer()
    class Meta:
        model = UserProfile
        fields = ['user','pk', 'profile_picture', 'iv']
class VlogSerializer(serializers.ModelSerializer):
    segments = SegmentSerializer(many=True, read_only=True)
    cipher_object = serializers.JSONField
    shared_with = serializers.CharField()
    class Meta:
        model = Vlog
        fields = ['playlist', "thumbnail", 'cipher_object', 'pk','segments','shared_with']

    def create(self, validated_data):
        vlog = Vlog.objects.create(playlist=validated_data['playlist'], thumbnail=validated_data['thumbnail'], cipher_object=validated_data['cipher_object'], user=self.context['request'].user.userprofile)
        shared_with_data = validated_data.pop('shared_with')
        if shared_with_data:
            shared_with_data = json.loads(shared_with_data)
            users = UserProfile.objects.filter(pk__in=shared_with_data)
            for userprofile in users:
                vlog.shared_with.add(userprofile)
                #FCM PUSH NOTIFICATION
                registration_id = userprofile.fcm_token
                message_title = self.context['request'].user.username
                message_body = "has shared a vlog with you"
                result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)
        segments_data = self.context.get('view').request.FILES
        for segment_data in segments_data.values():
            if segment_data.name.endswith(".ts"):
                Segment.objects.create(vlog=vlog, file=segment_data)
        vlog.save()
        return vlog


class VlogListSerializer(serializers.ModelSerializer):
    cipher_object = serializers.JSONField
    filename = serializers.SerializerMethodField()
    thumb_filename = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()
    user = UserProfileShareWithSerializer(read_only=True)
    class Meta:
        model = Vlog
        fields = ['user','playlist', "thumbnail", 'cipher_object', 'pk', 'filename', "thumb_filename", "type"]
    def get_type(self, obj):
        return "vlog"
    def get_filename(self, obj):
        return obj.playlist.name
    def get_thumb_filename(self, obj):
        return obj.thumbnail.name
