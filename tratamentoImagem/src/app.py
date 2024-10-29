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

def detect_and_crop_face(image, face_cascade, width=512, height=512):
    faces = face_cascade.detectMultiScale(image, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    if len(faces) == 0:
        print("Nenhum rosto encontrado na imagem")
        return None

    x, y, w, h = faces[0]  # Considera apenas o primeiro rosto detectado
    face = image[y:y+h, x:x+w]
    resized_face = cv2.resize(face, (width, height), interpolation=cv2.INTER_AREA)
    return resized_face

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

# Carrega o Haar Cascade para detecção de rosto
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

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
                
                cropped_face = detect_and_crop_face(grayscale_image, face_cascade)
                if cropped_face is not None:
                    processed_image_key = image_key  
                    cv2.imwrite(local_filename, cropped_face.astype(np.uint8))  
                    upload_image(bucket_staged, processed_image_key, local_filename)
                    print(f"Imagem {image_key} processada e salva no bucket consumed com foco no rosto")
            
            os.remove(local_filename)
