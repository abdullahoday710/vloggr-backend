from rest_framework import serializers
from .models import Vlog
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


class VlogSerializer(serializers.ModelSerializer):
    cipher_object = serializers.JSONField
    class Meta:
        model = Vlog
        fields = ['file', "thumbnail", 'cipher_object','pk']

    def create(self, validated_data):
        vlog = Vlog.objects.create(file=validated_data['file'], thumbnail=validated_data['thumbnail'], cipher_object=validated_data['cipher_object'], user=self.context['request'].user.userprofile)
        vlog.save()
        return vlog


class VlogListSerializer(serializers.ModelSerializer):
    cipher_object = serializers.JSONField
    filename = serializers.SerializerMethodField()
    thumb_filename = serializers.SerializerMethodField()
    class Meta:
        model = Vlog
        fields = ['file', "thumbnail", 'cipher_object', 'pk', 'filename', "thumb_filename"]

    def get_filename(self, obj):
        return obj.file.name
    def get_thumb_filename(self, obj):
        return obj.thumbnail.name
