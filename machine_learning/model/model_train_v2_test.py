import pickle
import numpy as np
from skimage.io import imread
from skimage.transform import resize
from skimage.feature import hog
import matplotlib.pyplot as plt

# Parâmetros
img_height, img_width = 150, 150
orientations = 9
pixels_per_cell = (8, 8)
cells_per_block = (2, 2)

# Função para processar uma nova imagem
def process_image(image_path):
    image = imread(image_path, as_gray=True)
    image_resized = resize(image, (img_height, img_width))
    hog_features = hog(image_resized, orientations=orientations, pixels_per_cell=pixels_per_cell, cells_per_block=cells_per_block, block_norm='L2-Hys')
    return hog_features

# Carregar o modelo salvo
model_file = 'acne_severity_model.pkl'
with open(model_file, 'rb') as file:
    model = pickle.load(file)

# Caminho da nova imagem
new_image_path = './modelo.jpg'  # Substitua pelo caminho da sua imagem

# Processar a nova imagem
features = process_image(new_image_path).reshape(1, -1)

# Fazer a previsão
prediction = model.predict(features)
severity = prediction[0]

# Mostrar o resultado
print(f"A severidade da acne na imagem é: {severity}")

# Opcional: Mostrar a imagem
image = imread(new_image_path)
plt.imshow(image, cmap='gray')
plt.title(f"Severidade da Acne: {severity}")
plt.axis('off')
plt.show()
