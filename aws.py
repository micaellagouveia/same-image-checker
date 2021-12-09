import boto3
import hashlib

# Escrevendo novo arquivo levando a pasta do imóvel correspondente
#def add_bucket_hash(hash: str, property_id: int):
s3 = boto3.resource('s3')
for bucket in s3.buckets.all():
    print(bucket.name)
property_id = 2
hash = '23e448eb5a55be340ebeef320f6897c8a17b0a259e4b1a124cc9c58215900e4f'
#data = open('test2.jpg', 'rb')

# File to check
file_name = 'test2.jpg'
 
with open(file_name, "rb") as f:
    file_hash = hashlib.md5()
    # This reads the file 8192 (or 2¹³) bytes at a time instead of all at once with f.read() to use less memory.
    while chunk := f.read(8192):
        file_hash.update(chunk)

print(file_hash.hexdigest())  # to get a printable str instead of bytes



#s3.Bucket('teste-media-hash').put_object(Key="company_01/property_01/image_02.jpeg", Body=data, Metadata={'hash':hash})

#return True



# Pegando dicionario com as hashes de um imóvel específico
#def get_bucket_hashes(property_id: int):
#    s3 = boto3.client('s3')
#
#    paginator = s3.get_paginator('list_objects_v2')
#    page_iterator = paginator.paginate(Bucket='teste-media-hash')
#    for bucket in page_iterator:
#        for image in bucket['Contents']:
#            print(image['Key'])
#            try:
#                metadata = s3.head_object(Bucket='teste-media-hash', Key=image['Key'])
#                print(metadata["ResponseMetadata"]['HTTPHeaders']['x-amz-meta-hash'])
#            except:
#                print("Failed {}".format(image['Key']))
#
#s3 = boto3.client('s3')
#params = {
#    "Bucket": "teste-media-hash",
#    "Prefix": f"{2}"
#}
#bucket = s3.list_objects_v2(**params)
#print(bucket)
#hashes = { d['Key'].split("/")[1] for d in bucket['Contents'] }
#print(hashes)

