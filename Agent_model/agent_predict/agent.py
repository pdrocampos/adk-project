from google.adk.agents import Agent
from google.adk.tools import FunctionTool
import joblib
import pandas as pd
from google.adk.agents import Agent
from google.adk.tools import FunctionTool

# Carregar pipeline e colunas salvas
pipeline = joblib.load('../output/modelo_financiamento.pkl')
columns = joblib.load('../output/colunas_modelo.pkl')

def preparar_dados_usuario(respostas: dict) -> dict:
    """
    Recebe um dict com respostas simples do usuário e converte para o formato técnico
    esperado pelo modelo.

    Exemplo de entrada:
    {
      "taxa_juros": "8",
      "tipo_imovel": "apartamento",
      "sistema_amortizacao": "price",
      "regiao": "pernambuco",
      "cotista_fgts": "não",
      "renda_familiar": "9000",
      "ano": "2025",
      "mes": "11"
    }

    Saída:
    {
      "num_taxa_juros": 8.0,
      "txt_tipo_imovel": "apartamento",
      "txt_sistema_amortizacao": "PRICE",
      "txt_regiao": "pernambuco",
      "bln_cotista": False,
      "vlr_renda_familiar": 9000.0,
      "num_taxa_juros_na": 0,
      "txt_sistema_amortizacao_na": "",
      "bln_cotista_na": False,
      "ano": 2025,
      "mes": 11
    }
    """

    # Mapeamento simples para booleano
    cotista = respostas.get("cotista_fgts", "").strip().lower()
    bln_cotista = cotista in ["sim", "s", "yes", "true", "1"]

    # Sistema amortização para maiúsculas, validar se é PRICE ou SAC
    sistema = respostas.get("sistema_amortizacao", "").strip().upper()
    if sistema not in ["PRICE", "SAC"]:
        sistema = "PRICE"  # default se inválido

    # Montar dict técnico
    dados_modelo = {
        "num_taxa_juros": float(respostas.get("taxa_juros", 0)),
        "txt_tipo_imovel": respostas.get("tipo_imovel", "").lower(),
        "txt_sistema_amortizacao": sistema,
        "txt_regiao": respostas.get("regiao", "").lower(),
        "bln_cotista": bln_cotista,
        "vlr_renda_familiar": float(respostas.get("renda_familiar", 0)),
        "num_taxa_juros_na": 0,
        "txt_sistema_amortizacao_na": "",
        "bln_cotista_na": False,
        "ano": int(respostas.get("ano", 2025)),
        "mes": int(respostas.get("mes", 1)),
    }

    return dados_modelo

def predict_financiamento(input_data: dict) -> dict:
    """
    input_data: dicionário com as features, ex:
    {
      "num_taxa_juros": 6.5,
      "txt_tipo_imovel": "apartamento",
      "txt_sistema_amortizacao": "SAC",
      "txt_regiao": "sudeste",
      "bln_cotista": True,
      "vlr_renda_familiar": 4500,
      "num_taxa_juros_na": 0,
      "txt_sistema_amortizacao_na": "",
      "bln_cotista_na": False,
      "ano": 2025,
      "mes": 8
    }
    """
    # Montar DataFrame no formato esperado pelo pipeline
    df_input = pd.DataFrame([input_data], columns=columns)
    # Fazer a predição
    pred = pipeline.predict(df_input)[0]
    # Retornar resultado como float para serialização JSON
    return {"vlr_financiamento_predito": float(pred)}

# Criar tool que chama a função de predição
predict_tool = FunctionTool(predict_financiamento)

# Criar agent com a tool
root_agent = Agent(
    model="gemini-2.0-flash", 
    name="fgts_financing_agent",
    description="Agent para prever valor de financiamento habitacional usando FGTS.",
    tools=[predict_tool]
)