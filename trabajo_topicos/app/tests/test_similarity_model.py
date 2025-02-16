
import pytest
import numpy as np
import networkx as nx
from app.main import app
from app.models.ml_model import run_similarity_model

@pytest.fixture
def sample_graphs():
    """Crea dos subgrafos en formato JSON para pruebas."""
    G1 = nx.Graph()
    G1.add_edges_from([("A", "B"), ("B", "C"), ("C", "D")])

    G2 = nx.Graph()
    G2.add_edges_from([("X", "Y"), ("Y", "Z"), ("Z", "W")])

    return [nx.node_link_data(G1), nx.node_link_data(G2)]  #  Devuelve JSON válido

def test_similarity_model(sample_graphs):
    """Valida que el modelo predice un valor entre 0 y 1 cuando recibe arrays."""
    result = run_similarity_model(sample_graphs)
    
    assert "probabilidad" in result
    assert isinstance(result["probabilidad"], float)
    assert 0 <= result["probabilidad"] <= 1
