from PIL.Image import Image
from rest_framework import serializers


class LinkSerializer(serializers.Serializer):
    link_1 = serializers.URLField()
    link_2 = serializers.URLField()

class ImageSerializer(serializers.Serializer):
    link = serializers.URLField()

class AddImageSerializer(serializers.Serializer):
    links = ImageSerializer(many=True)

class PropertySerializer(serializers.Serializer):
    property_id = serializers.IntegerField()
    medias = serializers.ListField()

class PropertiesSerializer(serializers.Serializer):
    properties = PropertySerializer(many=True)