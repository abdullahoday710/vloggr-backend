from rest_framework import serializers
from .models import Vlog,Segment
from users.models import UserProfile
import json

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

class UserProfileShareWithSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['pk']
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
            for user in users:
                vlog.shared_with.add(user)
                #TODO FCM PUSH NOTIFICATION
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
    class Meta:
        model = Vlog
        fields = ['playlist', "thumbnail", 'cipher_object', 'pk', 'filename', "thumb_filename", "type"]
    def get_type(self, obj):
        return "vlog"
    def get_filename(self, obj):
        return obj.playlist.name
    def get_thumb_filename(self, obj):
        return obj.thumbnail.name
