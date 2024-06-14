import boto3
import cv2
import os
import numpy as np
from botocore.exceptions import NoCredentialsError
from sklearn.decomposition import PCA


def download_image(bucket_name, image_key, local_filename):
    s3 = boto3.client('s3')
    try:
        s3.download_file(bucket_name, image_key, local_filename)
    except NoCredentialsError:
        print("Credenciais não configuradas corretamente ou não disponíveis")
        return False
    return True

def load_image_grayscale(filename):
    image = cv2.imread(filename)
    if image is None:
        print(f"Erro ao carregar a imagem {filename}")
        return None
    grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return grayscale_image


def apply_pca(image, variance_ratio=0.9):
    
    flat_image = image.flatten().astype(np.float32)
    
    pca = PCA(n_components=variance_ratio, svd_solver='full')
    transformed = pca.fit_transform(flat_image.reshape(1, -1))
    reconstructed = pca.inverse_transform(transformed)
    pca_image = reconstructed.reshape(image.shape)
    return pca_image


def resize_image(image, scale_percent=50):
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    dim = (width, height)
    resized = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
    return resized


def upload_image(bucket_name, image_key, local_filename):
    s3 = boto3.client('s3')
    try:
        s3.upload_file(local_filename, bucket_name, image_key)
    except NoCredentialsError:
        print("Credenciais não configuradas corretamente ou não disponíveis")


env = os.getenv('ENVIRONMENT', 'DEV')  # Por padrão, considere que não é PROD

if env != 'PROD':
    boto3.setup_default_session(profile_name="faculdade")

bucket_raw = 'tcc-dev-raw-bucket'
bucket_staged = 'tcc-dev-consumed-bucket'

s3 = boto3.resource('s3')


raw_bucket = s3.Bucket(bucket_raw)
raw_images = [obj.key for obj in raw_bucket.objects.all()]


staged_bucket = s3.Bucket(bucket_staged)
staged_images = [obj.key for obj in staged_bucket.objects.all()]


for image_key in raw_images:
    if image_key not in staged_images:
        local_filename = os.path.join('temp_image.jpg')
        
        if download_image(bucket_raw, image_key, local_filename):
            
            grayscale_image = load_image_grayscale(local_filename)
            if grayscale_image is not None:
                
                resized_image = resize_image(grayscale_image)
                
                pca_image = apply_pca(resized_image)
                
                processed_image_key = image_key  
                cv2.imwrite(local_filename, pca_image.astype(np.uint8))  
                upload_image(bucket_staged, processed_image_key, local_filename)
                print(f"Imagem {image_key} processada e salva no bucket staged")
            os.remove(local_filename)
