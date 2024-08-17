import boto3
import cv2
import os
import numpy as np
from botocore.exceptions import NoCredentialsError

def download_image(bucket_name, image_key, local_filename):
    s3 = boto3.client('s3')
    try:
        s3.download_file(bucket_name, image_key, local_filename)
        return True
    except NoCredentialsError:
        print("Credenciais não configuradas corretamente ou não disponíveis")
        return False

def detect_and_cover_eyes(image):
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

    eyes = eye_cascade.detectMultiScale(image, scaleFactor=1.07, minNeighbors=35, minSize=(50, 30))
    for (x, y, w, h) in eyes:
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 0), -1)
    
    return image

def convert_to_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def resize_image(image, output_size):
    resized_image = cv2.resize(image, output_size, interpolation=cv2.INTER_AREA)
    return resized_image

def upload_image(bucket_name, image_key, local_filename):
    s3 = boto3.client('s3')
    try:
        s3.upload_file(local_filename, bucket_name, image_key)
    except NoCredentialsError:
        print("Credenciais não configuradas corretamente ou não disponíveis")

def process_image(image_key, local_filename, bucket_staged):
    if download_image(bucket_raw, image_key, local_filename):
        image = cv2.imread(local_filename)
        if image is not None:
            #processed_image = detect_and_cover_eyes(image)  # Detecta e cobre os olhos na imagem colorida
            grayscale_image = convert_to_grayscale(image)  # Converte a imagem processada em escala de cinza
            resized_image = resize_image(grayscale_image, (512, 512))  # Redimensiona a imagem
            cv2.imwrite(local_filename, resized_image)
            upload_image(bucket_staged, image_key, local_filename)
            print(f"Imagem {image_key} processada e salva no bucket staged")
        os.remove(local_filename)

env = os.getenv('ENVIRONMENT', 'DEV')  # Por padrão, considere que não é PROD

boto3.setup_default_session(profile_name="faculdade")

bucket_raw = 'tcc-dev-raw-bucket'
bucket_consumed = 'tcc-dev-consumed-bucket'

s3 = boto3.resource('s3')
raw_images = [obj.key for obj in s3.Bucket(bucket_raw).objects.all()]
staged_images = {obj.key for obj in s3.Bucket(bucket_consumed).objects.all()}

for image_key in raw_images:
    if image_key not in staged_images:
        process_image(image_key, 'temp_image.jpg', bucket_consumed)