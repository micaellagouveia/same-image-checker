from copy import Error
import boto3
import uuid
from typing import List

from requests.exceptions import RequestException

from images_checker.images_checker import calculate_image_hash

# Escrevendo novo arquivo levando a pasta do imóvel correspondente
def add_bucket_hash(hash: str, property_id: int, company_id: int, file_name: str):
    s3 = boto3.resource('s3')

    try:
        data = open('/tmp/' + file_name, 'rb')
        s3.Bucket('teste-media-hash').put_object(
        Key=f"company_{company_id}/property_{property_id}/{file_name}.jpeg",
        Body=data,
        Metadata={'hash':hash})
    except RequestException as exc:
        raise Error("Falha na abertura do arquivo ou para salvar no bucket")
    return

# Generate hash
def generate_md5_hash(links: list):
    new_hashes = []
    for link in links:
        file_name = uuid.uuid4().hex[:5]
        image_hash = calculate_image_hash(link, '/tmp/' + file_name)
        new_hashes.append({'etag':image_hash, 'key': file_name})

    return new_hashes   


# Pegando todas as hashes de uma company
def get_all_bucket_hashes(company_id: int):
    s3 = boto3.client('s3')
    all_hashes = []

    bucket = s3.list_objects(Bucket='teste-media-hash', Prefix=f'company_{company_id}')
    if 'Contents' in bucket:
        for hash in bucket['Contents']:
            all_hashes.append({'key': hash['Key'], 'etag': hash['ETag']})
    
    return all_hashes

def filter_hashes_by_property(all_hashes: List[dict], property_id: int):
    filtered_hashes = [{
        'key': elem['key'],
        'etag': elem['etag']
        } for elem in all_hashes if f'property_{property_id}' in elem['key']]
    return filtered_hashes

# Deletando imagem no bucket
def delete_bucket_image(company_id: int, property_id: int, file_name: str):
    # TODO: verificar se está funcionando a função de deletar
    s3 = boto3.client('s3')
    try:
        s3.delete_object(
            Bucket='teste-media-hash',
            Key=f'company_{company_id}/property_{property_id}/{file_name}'
            )
    except RequestException as exc:
        raise Error('Falha ao deletar imagem no bucket')

# Pegando as hashes de um imóvel específico - DEPECRATED
def get_bucket_hashes_by_property(property_id: int):
    s3 = boto3.client('s3')
    hashes = []

    paginator = s3.get_paginator('list_objects_v2')
    page_iterator = paginator.paginate(Bucket='teste-media-hash', Prefix=f'{property_id}')
    
    for bucket in page_iterator:
        # print(bucket)
        if bucket['KeyCount'] > 0:
            for image in bucket['Contents']:
                # print(image['Key'])
                try:
                    metadata = s3.head_object(Bucket='teste-media-hash', Key=image['Key'])
                    hash = metadata['ResponseMetadata']['HTTPHeaders']['x-amz-meta-hash']
                    hashes.append(hash)
                    #hashes.append({"file_name": image['key'],"hash": hash})
                except:
                    print(f"Failed {image['Key']}")
    
    return hashes
