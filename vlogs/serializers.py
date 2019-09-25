from rest_framework import serializers
from .models import Vlog,Segment
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

class VlogSerializer(serializers.ModelSerializer):
    segments = SegmentSerializer(many=True, read_only=True)
    cipher_object = serializers.JSONField
    class Meta:
        model = Vlog
        fields = ['playlist', "thumbnail", 'cipher_object', 'pk','segments']

    def create(self, validated_data):
        vlog = Vlog.objects.create(playlist=validated_data['playlist'], thumbnail=validated_data['thumbnail'], cipher_object=validated_data['cipher_object'], user=self.context['request'].user.userprofile)
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
