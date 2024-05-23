import boto3
import logging

class StorageS3:

    def __init__(self, bucket_name: str, profile_name: str='faculdade') -> None:
        # boto3.setup_default_session(profile_name=profile_name) # uncooment to run local
        self.s3 = boto3.client('s3')
        self.bucket_name = bucket_name

    def download(self, file_path_s3: str, file_save: str):
        logging.info(f'Downloading file_path_s3={file_path_s3} to file_save={file_save}...')
        self.s3.download_file(self.bucket_name, file_path_s3, file_save)

    def list_all_files(self) -> list[str]:
        logging.info(f'Listing all files in bucket s3: {self.bucket_name}')
        paginator = self.s3.get_paginator('list_objects_v2')
        pages = paginator.paginate(Bucket=self.bucket_name)

        files_s3 = []
        for page in pages:
            for obj in page['Contents']:
                files_s3.append(obj['Key'])

        return sorted(files_s3, reverse=True)
    