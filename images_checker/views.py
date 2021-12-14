import threading
import uuid
from typing import List

from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view

from images_checker import serializers
from images_checker import models
from images_checker import aws
from images_checker.images_checker import is_same_image
from images_checker.images_checker import calculate_image_hash, delete_image

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
    bucket_hashes = aws.get_bucket_hashes_by_property(property.id)

    # Pegar lista de novos links e gerar hashes
    images_hashes = []
    for image_data in data['links']:
        link = image_data['link']

        file_name = uuid.uuid4().hex[:5]
        image_hash = calculate_image_hash(link, '/tmp/' + file_name)
        images_hashes.append(image_hash)

        # se a imagem dos links não está na lista do bucket -> add ao bucket
        if image_hash not in bucket_hashes:
            aws.add_bucket_hash(image_hash, property.id, file_name)

        delete_image(file_name)

    bucket_hashes = aws.get_bucket_hashes_by_property(property.id)

    for bucket_hash in bucket_hashes:
        # se a imagem do bucket não está na lista de links
        if bucket_hash not in images_hashes:
            pass # deletar imagem do bucket
    


    return Response({"bucket": bucket_hashes, "links": images_hashes })

@api_view(['POST'])
def add_all_images_bucket(request, company_id):
    serializer = serializers.PropertiesSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    company = get_object_or_404(models.Company, id=company_id)
    data = serializer.validated_data

    # Get all hashes from company
    all_hashes = aws.get_all_bucket_hashes(company_id)

    
    for property in data['properties']:
        # get hashes from property
        property_bucket_hashes = aws.filter_hashes_by_property(all_hashes, property['property_id']) 

        # Generate hash to new images coming
        new_hashes = aws.generate_md5_hash(property['medias'])

        # Generate sets of hashes
        set_bucket_hashes = { elem['etag'] for elem in property_bucket_hashes }
        set_new_hashes = { elem['etag'] for elem in new_hashes }

        for new_hash in new_hashes:
            # se a imagem dos links não está na lista do bucket -> add ao bucket
            if new_hash['etag'] not in set_bucket_hashes:
                aws.add_bucket_hash(new_hash['etag'], property['property_id'], company.id, new_hash['key'])
            
            delete_image(new_hash['key'])
        
        for bucket_hash in property_bucket_hashes:
            # se a imagem do bucket não está na lista de links -> deletar imagem do bucket
            if bucket_hash['etag'] not in set_new_hashes:
                aws.delete_bucket_image(bucket_hash['key'])

    return Response({"bucket": all_hashes })