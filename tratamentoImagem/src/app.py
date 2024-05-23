import boto3
import cv2
import os
import numpy as np
from botocore.exceptions import NoCredentialsError

boto3.setup_default_session(profile_name="faculdade")

# Função para baixar uma imagem do S3
def download_image(bucket_name, image_key, local_filename):
    boto3.setup_default_session(profile_name="faculdade")
    s3 = boto3.client('s3')
    try:
        s3.download_file(bucket_name, image_key, local_filename)
    except NoCredentialsError:
        print("Credenciais não configuradas corretamente ou não disponíveis")

# Função para carregar uma imagem em tons de cinza
def load_image_grayscale(filename):
    image = cv2.imread(filename)
    grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return grayscale_image

# Função para fazer upload de uma imagem para o S3
def upload_image(bucket_name, image_key, local_filename):
    boto3.setup_default_session(profile_name="faculdade")
    s3 = boto3.client('s3')
    try:
        s3.upload_file(local_filename, bucket_name, image_key)
    except NoCredentialsError:
        print("Credenciais não configuradas corretamente ou não disponíveis")

# Defina os nomes dos buckets da AWS
bucket_raw = 'tcc-dev-raw-bucket'
bucket_consumed = 'tcc-dev-consumed-bucket'

# Conecte-se ao serviço S3
s3 = boto3.resource('s3')

# Obtenha a lista de chaves de objetos no bucket raw
raw_bucket = s3.Bucket(bucket_raw)
raw_images = [obj.key for obj in raw_bucket.objects.all()]

# Obtenha a lista de chaves de objetos no bucket consumed
consumed_bucket = s3.Bucket(bucket_consumed)
consumed_images = [obj.key for obj in consumed_bucket.objects.all()]

# Verifique se há novas imagens no bucket raw
for image_key in raw_images:
    if image_key not in consumed_images:
        local_filename = 'temp_image.jpg'
        # Baixe a imagem do bucket raw
        download_image(bucket_raw, image_key, local_filename)
        # Carregue a imagem em tons de cinza
        grayscale_image = load_image_grayscale(local_filename)
        # Salve a imagem processada no bucket consumed
        processed_image_key = 'processed/' + image_key  # Adicione um prefixo para identificar imagens processadas
        cv2.imwrite(local_filename, grayscale_image)  # Sobrescreve a imagem original com a versão em tons de cinza
        upload_image(bucket_consumed, image_key, local_filename)
        print(f"Imagem {image_key} processada e salva no bucket consumed")
        os.remove(local_filename)