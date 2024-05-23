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

from integrations.storage_s3 import StorageS3
from enums.bucket_s3_enum import BucketS3Enum

class AcneService:

    def __init__(self) -> None:
        pass

    def predict_image_has_acne(self, image_path, model_path, img_size=(128, 128)) -> bool:
        model = joblib.load(model_path)

        img = imread(image_path)
        if img.ndim == 3:
            img = rgb2gray(img)
        img_resized = resize(img, img_size)
        hog_features = hog(img_resized, pixels_per_cell=(8, 8), cells_per_block=(2, 2), visualize=False)
        hog_features = np.array(hog_features).reshape(1, -1)
        
        prediction = model.predict(hog_features)
        if prediction[0] == 1:
            return True
        else:
            return False

    def get_acne_report(self, photo: UploadFile):
        logging.info(f'Generating acne report to {photo.filename}...')
        storage_s3 = StorageS3(bucket_name=BucketS3Enum.BUCKET_TRAINED_MODEL.value)
        files_s3 = storage_s3.list_all_files()

        try:        
            if files_s3:
                last_model_name = os.path.split(files_s3[0])[-1]
            else:
                raise HTTPException(404, 'Any model.pkl found in bucket...')

            tmp_dir = tempfile.mkdtemp(prefix='last_model_pkl')
            last_model_path = os.path.join(tmp_dir, last_model_name)
            storage_s3.download(last_model_name, last_model_path)

            with open(os.path.join(tmp_dir, photo.filename), 'wb') as tmp_file:
                tmp_file.write(photo.file.read())
            
            has_acne = self.predict_image_has_acne(os.path.join(tmp_dir, photo.filename), last_model_path)

            shutil.rmtree(tmp_dir)

            return {'status': has_acne, 'report': 'Você possí acne, recomendamos buscar um dermatologista!'}
        
        except Exception as e:
            if os.path.exists(tmp_dir):
                shutil.rmtree(tmp_dir)
            raise e
