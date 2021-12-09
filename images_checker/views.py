import threading
import uuid

from django.shortcuts import render

from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view

from images_checker import serializers
from images_checker.images_checker import is_same_image
from images_checker import models
from images_checker.images_checker import calculate_image_hash, delete_image
from images_checker.aws import add_bucket_hash, get_bucket_hashes_by_property, get_all_bucket_hashes


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
def add_image_bucket_by_property(request, property_id):
    serializer = serializers.AddImageSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    property = get_object_or_404(models.Property, id=property_id)
    data = serializer.validated_data

    # Pegar lista de hashes no bucket daquele imóvel
    bucket_hashes = get_bucket_hashes_by_property(property.id)
    # print(bucket_hashes)
    # print("------------------------------")

    # Pegar lista de novos links e gerar hashes
    images_hashes = []
    for image_data in data['links']:
        link = image_data['link']

        file_name = uuid.uuid4().hex[:5]
        image_hash = calculate_image_hash(link, '/tmp/' + file_name)
        images_hashes.append(image_hash)

        # se a imagem dos links não está na lista do bucket -> add ao bucket
        if image_hash not in bucket_hashes:
            add_bucket_hash(image_hash, property.id, file_name)

        delete_image(file_name)
    # print(images_hashes)
    # print("------------------------------")

    bucket_hashes = get_bucket_hashes_by_property(property.id)
    # print(bucket_hashes)
    # print("------------------------------")

    for bucket_hash in bucket_hashes:
        # se a imagem do bucket não está na lista de links
        if bucket_hash not in images_hashes:
            pass # deletar imagem do bucket
    


    return Response({"bucket": bucket_hashes, "links": images_hashes })

@api_view(['POST'])
def add_all_images_bucket(request, company_id):
    #serializer = serializers.PropertiesSerializer(data=request)
    #serializer.is_valid(raise_exception=True)
    #company = get_object_or_404(models.Company, id=company_id)
    #data = serializer.validated_data

    # Get all hashes from company
    hashes = get_all_bucket_hashes(company_id)
    return Response({"bucket": hashes })