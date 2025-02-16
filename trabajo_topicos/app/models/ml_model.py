import tensorflow as tf
import numpy as np
import networkx as nx
from sklearn.preprocessing import StandardScaler

# Crear y cargar modelo de red neuronal para similitud
def create_similarity_model(input_dim=4):
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(16, activation="relu", input_shape=(input_dim,)),
        tf.keras.layers.Dense(8, activation="relu"),
        tf.keras.layers.Dense(1, activation="sigmoid")  # Salida entre 0 y 1
    ])
    model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])
    return model

#  Inicializar y cargar modelo (en un futuro puedes cargar pesos entrenados)
model = create_similarity_model()
scaler = StandardScaler()  # Inicializa el escalador una sola vez

def extract_graph_features(graph):
    """
    Extrae características de un grafo para convertirlo en un vector.
    """
    num_nodes = graph.number_of_nodes()
    num_edges = graph.number_of_edges()
    avg_degree = np.mean([d for _, d in graph.degree()]) if num_nodes > 0 else 0
    clustering_coefficient = nx.average_clustering(graph) if num_nodes > 1 else 0
    return np.array([num_nodes, num_edges, avg_degree, clustering_coefficient])

def preprocess_graphs(graphs):
    """
    Convierte una lista de grafos en una matriz de características normalizada.
    """
    features = np.array([extract_graph_features(g) for g in graphs])
    return scaler.fit_transform(features)  # Ajusta una vez en la inicialización

import traceback  #  Para capturar el stack trace

def run_similarity_model(graph_inputs):
    """
    Recibe dos grafos en JSON, extrae características y usa la red neuronal para predecir similitud.
    """
    try:
        print(f" Recibido graph_inputs: {graph_inputs}")

        # Convertir JSON a grafos de NetworkX y forzar a `Graph` en lugar de `MultiGraph`
        G1 = nx.Graph(nx.node_link_graph(graph_inputs[0], edges="links"))
        G2 = nx.Graph(nx.node_link_graph(graph_inputs[1], edges="links"))

        print(f" Grafos convertidos: {G1.number_of_nodes()} nodos, {G2.number_of_nodes()} nodos")

        # Extraer características y preprocesar
        vec1, vec2 = preprocess_graphs([G1, G2])
        input_data = np.abs(vec1 - vec2).reshape(1, -1)

        print(f" Datos de entrada procesados: {input_data}")

        # Realizar predicción con el modelo
        probabilidad = model.predict(input_data)[0][0]

        print(f" Predicción realizada: {probabilidad}")

        return {"probabilidad": round(float(probabilidad), 2)}

    except Exception as e:
        error_trace = traceback.format_exc()
        print(f" Error en la ejecución del modelo:\n{error_trace}")
        return {"error": f"Error en la ejecución del modelo: {str(e)}"}
