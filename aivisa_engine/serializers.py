from rest_framework import serializers

from .models import Photo


class ProcessPhotoInputSerializer(serializers.Serializer):
    photo = serializers.ImageField(required=True, allow_empty_file=False)
    width = serializers.IntegerField(required=True)
    height = serializers.IntegerField(required=True)
    red = serializers.IntegerField(required=False, min_value=0, max_value=255)
    green = serializers.IntegerField(required=False, min_value=0, max_value=255)
    blue = serializers.IntegerField(required=False, min_value=0, max_value=255)
    enhance = serializers.BooleanField(required=False)


class PhotoModelSerializer(serializers.ModelSerializer):

    class Meta:
        fields = [
            'uuid',
            'photo',
            'title',
            'width',
            'height',
            'single',
            'multi'
        ]

        model = Photo
