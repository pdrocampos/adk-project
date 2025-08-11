from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from tools.tool import predict_financing


root_agent = Agent(
    model="gemini-2.0-flash",  # ou outro modelo Gemini que preferir
    name="financing_agent",
    description="Agente que prevê valor de financiamento baseado em dados estruturados",
    instruction="Use a função predict_financing para estimar o valor, conforme os dados fornecidos.",
    tools=[FunctionTool(predict_financing)]
)