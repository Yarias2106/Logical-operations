import pandas as pd
import os

#Preparamos nuestro dataset
dataset = pd.read_csv('Operaciones Logicas.csv')
X = dataset.iloc[: , 0:3].values
y = dataset.iloc[: , 3].values
#Escalamos nuestros datos
from sklearn.preprocessing import StandardScaler
sc_X = StandardScaler()
X_train = sc_X.fit_transform(X)

from keras.models import Sequential
from keras.layers import Dense

# Inicializamos la Red Neuronal
rna = Sequential()
# Añadimos las capas de entrada y primera capa oculta
rna.add(Dense(units = 7, kernel_initializer = "uniform",  activation = "relu", input_dim = 3))
# Añadimos la segunda capa oculta
rna.add(Dense(units = 7, kernel_initializer = "uniform",  activation = "relu"))
# Añadir la capa de salida
rna.add(Dense(units = 1, kernel_initializer = "uniform",  activation = "sigmoid"))
# Compilamos la Red Neuronal
rna.compile(optimizer = "adam", loss = "binary_crossentropy", metrics = ["accuracy"])
# Ajustamos la RNA al Conjunto de Entrenamiento
rna.fit(X_train, y,  batch_size = 11, epochs = 400)

#Guardamos el modelo entrenado
target_dir = './modelo/'
if not os.path.exists(target_dir):
  os.mkdir(target_dir)
rna.save('./modelo/modelo.h5')
rna.save_weights('./modelo/pesos.h5')
