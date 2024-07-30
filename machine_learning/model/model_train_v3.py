import os
import numpy as np
from skimage.io import imread
from skimage.transform import resize
from skimage.feature import hog
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, f1_score, recall_score, confusion_matrix
import pickle
import matplotlib.pyplot as plt
import seaborn as sns

# Diretório das imagens
data_dir = 'images_aws'

# Parâmetros
img_height, img_width = 150, 150
orientations = 9
pixels_per_cell = (8, 8)
cells_per_block = (2, 2)

# Função para carregar e processar as imagens
def load_images(data_dir):
    images = []
    labels = []
    for label in os.listdir(data_dir):
        label_dir = os.path.join(data_dir, label)
        if os.path.isdir(label_dir):
            for img_file in os.listdir(label_dir):
                img_path = os.path.join(label_dir, img_file)
                image = imread(img_path, as_gray=True)
                image_resized = resize(image, (img_height, img_width))
                hog_features = hog(image_resized, orientations=orientations, pixels_per_cell=pixels_per_cell, cells_per_block=cells_per_block, block_norm='L2-Hys')
                images.append(hog_features)
                labels.append(int(label.split()[-1]))  # Assuming folder names are 'Severidade 0', 'Severidade 1', etc.
    return np.array(images), np.array(labels)

# Carregar e processar as imagens
X, y = load_images(data_dir)

# Dividir os dados em conjuntos de treino e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Definir os parâmetros para o GridSearchCV
param_grid = {
    'n_estimators': list(range(1, 150, 10)),
    'criterion': ['gini', 'entropy'],
    'max_depth': list(range(1, 16))
}

# Criar o modelo de Random Forest
clf = RandomForestClassifier(random_state=42)

# Configurar o GridSearchCV
grid_search = GridSearchCV(estimator=clf, param_grid=param_grid, cv=5, scoring='accuracy', n_jobs=-1)

# Treinar o modelo com GridSearchCV
grid_search.fit(X_train, y_train)

# Obter os melhores parâmetros
best_params = grid_search.best_params_
print(f"Best parameters found: {best_params}")

# Treinar o modelo final com os melhores parâmetros
best_clf = grid_search.best_estimator_
best_clf.fit(X_train, y_train)

# Avaliar o modelo final
y_pred = best_clf.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, average='weighted')
f1 = f1_score(y_test, y_pred, average='weighted')
recall = recall_score(y_test, y_pred, average='weighted')
print(f"Final Model - Accuracy: {accuracy * 100:.2f}%, Precision: {precision * 100:.2f}%, F1 Score: {f1 * 100:.2f}%, Recall: {recall * 100:.2f}%")

# Gerar a matriz de confusão
cm = confusion_matrix(y_test, y_pred)
print("Confusion Matrix:")
print(cm)

# Plotar a matriz de confusão
plt.figure(figsize=(10, 7))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=[f'Severidade {i}' for i in range(5)], yticklabels=[f'Severidade {i}' for i in range(5)])
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('Confusion Matrix')
plt.show()

# Salvar o modelo final
model_file = 'acne_severity_model.pkl'
with open(model_file, 'wb') as file:
    pickle.dump(best_clf, file)

print(f"Modelo salvo em {model_file}")
