import numpy as np
import os
from skimage.io import imread
from skimage.transform import resize
from skimage.feature import hog
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
import boto3
import shutil
import joblib
from datetime import datetime
import pathlib
from skimage.color import rgb2gray

try:
    boto3.setup_default_session(profile_name="faculdade") #TODO: remove in production
    s3 = boto3.client('s3')
    bucket_consumed = 'tcc-dev-consumed-bucket'
    bucket_model = 'tcc-dev-saved-model-bucket'

    paginator = s3.get_paginator('list_objects_v2')
    pages = paginator.paginate(Bucket=bucket_consumed)

    files_s3 = []
    for page in pages:
        for obj in page['Contents']:
            files_s3.append(obj['Key'])

    # Ajuste para nova estrutura de pastas
    files_no_acne = [f for f in files_s3 if str(f).startswith('SemAcne/') and f != 'SemAcne/']
    severity_levels = ['severity_1', 'severity_2', 'severity_3', 'severity_4']
    files_severity = {level: [f for f in files_s3 if str(f).startswith(f'{level}/') and f != f'{level}/'] for level in severity_levels}

    folders_imgs = ['SemAcne'] + severity_levels

    def download_list_files_s3(files: list, bucket_name: str, save_dir=''):
        save_dir = os.path.join('svm', save_dir)
        if not os.path.exists(save_dir):
            pathlib.Path(save_dir).mkdir(parents=True, exist_ok=True)
            
        for f in files:
            print(f'Downloading file={f}')
            s3.download_file(bucket_name, f, os.path.join(save_dir, os.path.split(f)[-1]))

    download_list_files_s3(files_no_acne, bucket_consumed, 'SemAcne')
    for level in severity_levels:
        download_list_files_s3(files_severity[level], bucket_consumed, level)

    def load_data(data_dir, img_size=(128, 128)):
        labels = []
        features = []
        label_map = {'SemAcne': 0, 'severity_1': 1, 'severity_2': 2, 'severity_3': 3, 'severity_4': 4}
        for label in label_map.keys():
            folder = os.path.join(data_dir, label)
            for file in os.listdir(folder):
                img_path = os.path.join(folder, file)
                img = imread(img_path)
                if img.ndim == 3:
                    img = rgb2gray(img)
                img_resized = resize(img, img_size)
                hog_features = hog(img_resized, pixels_per_cell=(8, 8), cells_per_block=(2, 2), visualize=False)
                features.append(hog_features)
                labels.append(label_map[label])
        return np.array(features), np.array(labels)

    # Carregar dados
    print('Training model...')
    data_dir = 'svm'
    X, y = load_data(data_dir)

    # Dividir os dados em conjuntos de treino e teste
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, train_size=0.2)

    # Treinar um classificador SVM não linear (RBF kernel)
    clf = SVC(kernel='rbf')
    clf.fit(X_train, y_train)

    # Avaliar o modelo
    y_pred = clf.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f'Accuracy: {accuracy * 100:.2f}%')

    # Salvar o modelo
    model_file = f"{datetime.now().strftime('%d-%m-%Y %H-%M-%S.%f')} svm_model.pkl"
    joblib.dump(clf, model_file)
    print(f'Model saved {model_file}')

    # Upando novo modelo treinado para bucket s3
    print(f'Uploading model to s3: {model_file}')
    s3.upload_file(model_file, bucket_model, model_file)

    print('Cleaning files model')
    shutil.rmtree(data_dir)
    os.remove(model_file)

except Exception as e:
    print('Cleaning files model')
    if os.path.exists(data_dir):
        shutil.rmtree(data_dir)
    if os.path.exists(model_file):
        os.remove(model_file)
    raise e
