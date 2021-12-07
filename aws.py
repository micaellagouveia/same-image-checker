import boto3

# Escrevendo novo arquivo 
def add_bucket_hash(hash: str):
    s3 = boto3.resource('s3')

    # for bucket in s3.buckets.all():
    #     print(bucket.name)
    
    # data = open('test.jpeg', 'rb')
    s3.Bucket('teste-media-hash').put_object(Key=hash)


# Pegando dicionario com os arquivos do bucket
def get_bucket_hashes():
    s3 = boto3.client('s3')
    bucket = s3.list_objects(Bucket='teste-media-hash')

    hashes = { d['Key'] for d in bucket['Contents'] }

    return hashes