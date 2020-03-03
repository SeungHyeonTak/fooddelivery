from storages.backends.s3boto3 import S3Boto3Storage


class MediaStorage(S3Boto3Storage):
    location = 'media'
    file_overwrite = False
    bucket_name = 'media.fooddeliverybackend.online'

    region_name = 'ap-northeast-2'
    custom_domain = 's3.%s.amazonaws.com/%s' % (region_name, bucket_name)
    # Route 53 연결 시, custom_domain 을 bucket_name으로 설정
    # custom_domain = bucket_name
