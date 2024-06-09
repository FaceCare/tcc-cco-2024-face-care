import boto3
import cv2
import os
import numpy as np
from PIL import Image
from botocore.exceptions import NoCredentialsError
from sklearn.decomposition import PCA

# Função para baixar uma imagem do S3
def download_image(bucket_name, image_key, local_filename):
    s3 = boto3.client('s3')
    try:
        s3.download_file(bucket_name, image_key, local_filename)
    except NoCredentialsError:
        print("Credenciais não configuradas corretamente ou não disponíveis")
        return False
    return True

# Função para carregar uma imagem em tons de cinza
def load_image_grayscale(filename):
    try:
        image = Image.open(filename).convert('L')
        img_array = np.array(image)
        return img_array
    except Exception as e:
        print(f"Erro ao carregar a imagem {filename}: {e}")
        return None

# Função para aplicar PCA
def apply_pca(image, n_components=30):
    original_img = Image.open(image).convert('L')
    img_array = np.array(original_img)

    original_components = img_array.shape[1]

    n_components = n_components

    pca = PCA(n_components=n_components)
    pca.fit(img_array)
    img_transformed = pca.transform(img_array)
    img_reconstructed = pca.inverse_transform(img_transformed)
    processed_components = pca.n_components_
    return img_reconstructed

# Função para fazer upload de uma imagem para o S3
def upload_image(bucket_name, image_key, local_filename):
    s3 = boto3.client('s3')
    try:
        s3.upload_file(local_filename, bucket_name, image_key)
    except NoCredentialsError:
        print("Credenciais não configuradas corretamente ou não disponíveis")

# Defina os nomes dos buckets da AWS
bucket_raw = 'tcc-dev-raw-bucket'
bucket_staged = 'tcc-dev-staged-bucket'

# Conecte-se ao serviço S3
s3 = boto3.resource('s3')

# Obtenha a lista de chaves de objetos no bucket raw
raw_bucket = s3.Bucket(bucket_raw)
raw_images = [obj.key for obj in raw_bucket.objects.all()]

# Obtenha a lista de chaves de objetos no bucket staged
staged_bucket = s3.Bucket(bucket_staged)
staged_images = [obj.key for obj in staged_bucket.objects.all()]

# Verifique se há novas imagens no bucket raw
for image_key in raw_images:
    if image_key not in staged_images:
        local_filename = 'temp_image.jpg'
        # Baixe a imagem do bucket raw
        if download_image(bucket_raw, image_key, local_filename):
            # Verifique se a imagem foi baixada corretamente
            if os.path.getsize(local_filename) > 0:
                # Carregue a imagem em tons de cinza
                grayscale_image = load_image_grayscale(local_filename)
                if grayscale_image is not None:
                    # Aplique PCA
                    pca_image = apply_pca(grayscale_image)
                    # Converta para uint8
                    pca_image_uint8 = pca_image.astype(np.uint8)
                    # Salve a imagem processada no bucket staged
                    processed_image_key = image_key  # Preserve a estrutura do caminho
                    Image.fromarray(pca_image_uint8).save(local_filename)  # Salva a imagem PCA
                    upload_image(bucket_staged, processed_image_key, local_filename)
                    print(f"Imagem {image_key} processada e salva no bucket staged")
                os.remove(local_filename)
            else:
                print(f"Falha ao baixar a imagem {image_key}")
