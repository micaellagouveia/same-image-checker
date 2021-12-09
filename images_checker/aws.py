import boto3

# Escrevendo novo arquivo levando a pasta do imóvel correspondente
def add_bucket_hash(hash: str, property_id: int, file_name: str):
    s3 = boto3.resource('s3')

    try:
        data = open('/tmp/' + file_name, 'rb')
        s3.Bucket('teste-media-hash').put_object(Key=f"{property_id}/{file_name}.jpeg", Body=data, Metadata={'hash':hash})
    except:
        print("Erro ao adicionar arquivo no bucket")
    
    return


# Pegando todas as hashes de uma company
def get_all_bucket_hashes(company_id: int):
    s3 = boto3.client('s3')
    all_hashes = []

    bucket = s3.list_objects(Bucket='teste-media-hash', Prefix=f'company_0{company_id}')
    print(bucket)
    if len(bucket['Contents']) > 0:
        for hash in bucket['Contents']:
            all_hashes.append({'key': hash['Key'], 'etag': hash['ETag']})
    
    # [elem for elem in l if 'property_01' in elem]

    return all_hashes

# Pegando as hashes de um imóvel específico
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

#s3 = boto3.client('s3')
#params = {
#    "Bucket": "teste-media-hash",
#    "Prefix": f"{2}"
#}
#bucket = s3.list_objects_v2(**params)
#print(bucket)
#hashes = { d['Key'].split("/")[1] for d in bucket['Contents'] }
#print(hashes)