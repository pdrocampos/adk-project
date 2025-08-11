import pickle
import pandas as pd

def predict_financing(data: dict) -> dict:
    """
    Recebe dicionário com dados de entrada, aplica o pipeline
    (estrutura de colunas, preprocessamento, etc.) e retorna
    a previsão do valor de financiamento.
    
    Args:
        data: dict — chaves e valores correspondentes às colunas esperadas.

    Returns:
        dict com a chave "prediction" e o valor previsto.
    """
    # Carrega modelo e colunas
    with open("modelo.pkl", "rb") as f:
        modelo = pickle.load(f)
    with open("colunas.pkl", "rb") as f:
        colunas = pickle.load(f)

    df = pd.DataFrame([data])
    df = df[colunas]  # garante mesma ordem/colunas
    pred = modelo.predict(df)[0]
    return {"prediction": float(pred)}