import threading

from django.shortcuts import render

from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view

from images_checker import serializers
from images_checker.images_checker import is_same_image
from images_checker import models
from images_checker.images_checker import calculate_image_hash


@api_view(['POST'])
def check_image(request):
    serializer = serializers.LinkSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    link_1 = serializer.validated_data['link_1']
    link_2 = serializer.validated_data['link_2']

    result = is_same_image(link_1, link_2)

    return Response({'result': result})

@api_view(['POST'])
def add_image(request, property_id):
    serializer = serializers.AddImageSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    #property = models.Property.objects.get(id=property_id)
    property = get_object_or_404(models.Property, id=property_id)
    data = serializer.validated_data

    threads: List[threading.Thread] = []

    for image_data in data['links']:
        link = image_data['link']

        thread = threading.Thread(
            target=models.Image.check_and_save_image,
            kwargs={ "link": link, "property": property, },
        )
        thread.start()
        threads.append(thread)
    
    thread: threading.Thread
    for thread in threads:
        thread.join()

    return Response({'result': True})


@api_view(['POST'])
def add_image_bucket(request, property_id):
    serializer = serializers.AddImageSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    #property = models.Property.objects.get(id=property_id)
    property = get_object_or_404(models.Property, id=property_id)
    data = serializer.validated_data

    threads: List[threading.Thread] = []

    for image_data in data['links']:
        link = image_data['link']

        thread = threading.Thread(
            target=models.Image.check_and_save_image,
            kwargs={ "link": link, "property": property, },
        )
        thread.start()
        threads.append(thread)
    
    thread: threading.Thread
    for thread in threads:
        thread.join()

    return Response({'result': True})