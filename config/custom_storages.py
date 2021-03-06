from storages.backends.s3boto3 import S3Boto3Storage, S3StaticStorage


class UploadStorage(S3Boto3Storage):
    location = "uploads/"


class StaticStorage(S3StaticStorage):
    location = "static/"
    file_overwrite = False