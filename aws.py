import boto3

# Escrevendo novo arquivo levando a pasta do imóvel correspondente
#def add_bucket_hash(hash: str, property_id: int):
#    s3 = boto3.resource('s3')
#    # for bucket in s3.buckets.all():
#    #     print(bucket.name)
#    # property_id = 2
#    # hash = '23e448eb5a55be340ebeef320f6897c8a17b0a259e4b1a124cc9c58215900e4f'
#    data = open('test.jpeg', 'rb')
#    s3.Bucket('teste-media-hash').put_object(Key=f"{property_id}/1.jpeg", Body=data, Metadata={'hash':hash})
#    return True



# Pegando dicionario com as hashes de um imóvel específico
def get_bucket_hashes(property_id: int):
    s3 = boto3.client('s3')

    paginator = s3.get_paginator('list_objects_v2')
    page_iterator = paginator.paginate(Bucket='teste-media-hash')
    for bucket in page_iterator:
        for image in bucket['Contents']:
            print(image['Key'])
            try:
                metadata = s3.head_object(Bucket='teste-media-hash', Key=image['Key'])
                print(metadata["ResponseMetadata"]['HTTPHeaders']['x-amz-meta-hash'])
            except:
                print("Failed {}".format(image['Key']))

#s3 = boto3.client('s3')
#params = {
#    "Bucket": "teste-media-hash",
#    "Prefix": f"{2}"
#}
#bucket = s3.list_objects_v2(**params)
#print(bucket)
#hashes = { d['Key'].split("/")[1] for d in bucket['Contents'] }
#print(hashes)

