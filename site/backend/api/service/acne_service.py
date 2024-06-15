import logging
import tempfile
import os
import numpy as np
import joblib
import shutil
from skimage.io import imread
from skimage.transform import resize
from skimage.feature import hog
from skimage.color import rgb2gray
from fastapi import UploadFile
from fastapi.exceptions import HTTPException
from datetime import datetime

from integrations.storage_s3 import StorageS3
from enums.bucket_s3_enum import BucketS3Enum

class AcneService:

    def __init__(self) -> None:
        pass

    def predict_image_severity(self, image_path, model_path, img_size=(128, 128)) -> int:
        model = joblib.load(model_path)

        img = imread(image_path)
        if img.ndim == 3:
            img = rgb2gray(img)
        img_resized = resize(img, img_size)
        hog_features = hog(img_resized, pixels_per_cell=(8, 8), cells_per_block=(2, 2), visualize=False)
        hog_features = np.array(hog_features).reshape(1, -1)
        
        prediction = model.predict(hog_features)
        return prediction[0]

    def get_acne_report(self, photo: UploadFile):
        logging.info(f'Generating acne report for {photo.filename}...')
        storage_s3 = StorageS3(bucket_name=BucketS3Enum.BUCKET_TRAINED_MODEL.value)
        files_s3 = storage_s3.list_all_files()

        def extract_datetime_from_filename(filename):
            try:
                timestamp_str = filename.split(' svm_model.pkl')[0]
                return datetime.strptime(timestamp_str, '%d-%m-%Y %H-%M-%S.%f')
            except ValueError as e:
                logging.error(f'Error parsing datetime from filename {filename}: {e}')
                return datetime.min

        try:
            if files_s3:
                # Ordenar arquivos pelo timestamp no nome
                files_s3.sort(key=extract_datetime_from_filename, reverse=True)
                last_model_name = os.path.split(files_s3[0])[-1]
            else:
                raise HTTPException(404, 'No model.pkl found in bucket...')

            tmp_dir = tempfile.mkdtemp(prefix='last_model_pkl')
            last_model_path = os.path.join(tmp_dir, last_model_name)
            storage_s3.download(last_model_name, last_model_path)

            with open(os.path.join(tmp_dir, photo.filename), 'wb') as tmp_file:
                tmp_file.write(photo.file.read())
            
            severity = self.predict_image_severity(os.path.join(tmp_dir, photo.filename), last_model_path)

            shutil.rmtree(tmp_dir)

            severity_messages = {
                0: 'Você não possuí acne, tudo normal por aqui!',
                1: 'Você possuí acne leve (grau 1), recomendamos buscar um dermatologista!',
                2: 'Você possuí acne moderada (grau 2), recomendamos buscar um dermatologista!',
                3: 'Você possuí acne grave (grau 3), recomendamos buscar um dermatologista!',
                4: 'Você possuí acne muito grave (grau 4), recomendamos buscar um dermatologista!'
            }

            report_msg = severity_messages.get(severity, 'Severidade desconhecida. Por favor, consulte um dermatologista.')

            return {'status': severity != 0, 'severity': severity, 'report': report_msg}
        
        except Exception as e:
            if os.path.exists(tmp_dir):
                shutil.rmtree(tmp_dir)
            raise e
