"""
chat_langgraph.py
Exemplo: LangGraph + LM Studio (gpt-oss-20b) + ViaCEP + clima mockado.
Rodar: python chat_langgraph.py
"""

from typing import Optional, Dict, Any
import re
import requests

# LangGraph / LangChain imports
from langchain.chat_models import init_chat_model
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent

# ---------- Configurações ----------
LM_STUDIO_BASE = "http://localhost:1234/v1"  # ajuste se necessário
LM_STUDIO_API_KEY = "lm-studio"  # pode ser qualquer string para LM Studio compatível
MODEL_NAME = "openai/gpt-oss-20b"  # conforme solicitado
# ------------------------------------

# Inicializa o LLM via LangChain helper (usa a API compatível OpenAI do LM Studio).
# init_chat_model padroniza a criação de modelos (aceita base_url para provedores compatíveis).
llm = init_chat_model(
    model=MODEL_NAME,
    model_provider="openai",
    base_url=LM_STUDIO_BASE,
    api_key=LM_STUDIO_API_KEY,
    temperature=0.0,
)

# ---------- Tools / Funções expostas ao agente ----------

@tool
def viacep_lookup(cep: str) -> Dict[str, Any]:
    """
    Consulta ViaCEP (https://viacep.com.br/ws/{cep}/json/).
    Retorna dicionário com dados do endereco ou {'error': '...'}.
    """
    cep_digits = re.sub(r"\D", "", cep)
    if not re.fullmatch(r"\d{8}", cep_digits):
        return {"error": "CEP inválido. Use 8 dígitos (ex: 01001000)."}
    url = f"https://viacep.com.br/ws/{cep_digits}/json/"
    try:
        resp = requests.get(url, timeout=6)
        resp.raise_for_status()
        data = resp.json()
        if data.get("erro"):
            return {"error": "CEP não encontrado."}
        # Retorna dados chaveados (uf, localidade, logradouro, bairro, etc.)
        return {
            "cep": data.get("cep"),
            "logradouro": data.get("logradouro"),
            "complemento": data.get("complemento"),
            "bairro": data.get("bairro"),
            "localidade": data.get("localidade"),
            "uf": data.get("uf"),
            "ibge": data.get("ibge"),
            "gia": data.get("gia"),
        }
    except Exception as e:
        return {"error": f"Erro ao consultar ViaCEP: {str(e)}"}

@tool
def mock_weather(city: str, state: Optional[str] = None) -> Dict[str, Any]:
    """
    Mock de serviço de clima. Retorna resposta estruturada.
    Substitua por integração com API de clima real (OpenWeatherMap, ClimaTempo, etc.)
    """
    # Mock simples
    return {
        "location": f"{city}" + (f", {state}" if state else ""),
        "temperature_c": 25,
        "condition": "Ensolarado (mock)",
        "humidity_pct": 60,
        "note": "Dados mockados — substitua por sua API de clima."
    }

# ---------- Cria o agente (ReAct) com ferramentas ----------
# create_react_agent recebe um llm (BaseLanguageModel) e a lista de tools
agent = create_react_agent(
    llm,
    tools=[viacep_lookup, mock_weather],
    prompt="Você é um assistente útil. Use as ferramentas disponíveis quando necessário."
)

# ---------- Orquestrador simples (interpreta input e faz chamadas diretas quando desejado) ----------
CEP_REGEX = re.compile(r"\b(\d{5}-?\d{3}|\d{8})\b")

def handle_user_message(user_text: str) -> str:
    """
    Regras:
    - Se usuário pedir 'endereço' ou enviar um CEP: usar viaCEP (viacep_lookup).
    - Se pedir 'clima' com 'cep' (ex: 'clima do cep 01001000'): -> viacep_lookup -> mock_weather.
    - Se pedir 'clima' com cidade/estado (ex: 'clima em São Paulo, SP'): usar mock_weather.
    - Caso contrário: delegar ao agente (que pode chamar ferramentas se necessário).
    """
    text_lower = user_text.lower()

    # 1) Caso: clima solicitado por CEP
    m_cep = CEP_REGEX.search(user_text)
    if "clima" in text_lower and m_cep:
        cep = m_cep.group(1)
        addr = viacep_lookup(cep)
        if "error" in addr:
            return f"Não consegui obter cidade a partir do CEP: {addr['error']}"
        city = addr.get("localidade")
        state = addr.get("uf")
        weather = mock_weather(city or "", state or "")
        return (
            f"Clima para {city}, {state} (obtido via CEP {cep}):\n"
            f"- Condição: {weather['condition']}\n"
            f"- Temperatura (°C): {weather['temperature_c']}\n"
            f"- Umidade: {weather['humidity_pct']}%\n"
            f"OBS: dados mockados."
        )

    # 2) Caso: consulta de endereço por CEP explícito
    if "cep" in text_lower or CEP_REGEX.search(user_text):
        if m_cep:
            cep = m_cep.group(1)
            addr = viacep_lookup(cep)
            if "error" in addr:
                return f"Erro: {addr['error']}"
            # Formata resposta amigável
            return (
                f"Endereço para CEP {cep}:\n"
                f"{addr.get('logradouro') or ''} {addr.get('complemento') or ''}\n"
                f"{addr.get('bairro') or ''} - {addr.get('localidade') or ''}/{addr.get('uf') or ''}"
            )
        # se menciona 'cep' sem dígitos, pede o CEP
        return "Você mencionou 'CEP'. Por favor informe o CEP (8 dígitos)."

    # 3) Caso: clima por cidade, ex: "Qual o clima em São Paulo, SP?"
    if "clima" in text_lower:
        # tenta extrair "cidade, UF" simples via vírgula
        m = re.search(r"clima.*em\s+([^\n,]+)(?:,\s*([A-Za-z]{2}))?", user_text, re.I)
        if m:
            city = m.group(1).strip()
            state = m.group(2).strip() if m.group(2) else None
            weather = mock_weather(city, state)
            return (
                    f"Clima para {city}" + (f", {state}" if state else "") + " (mock):\n"
                                                                             f"- Condição: {weather['condition']}\n"
                                                                             f"- Temperatura: {weather['temperature_c']} °C\n"
                                                                             f"- Umidade: {weather['humidity_pct']}%\n"
                                                                             f"OBS: dados mockados."
            )

    # 4) Fallback: use o agente (ReAct). O agente poderá chamar as tools se entender necessário.
    #    Passamos a mensagem como 'messages' (formato esperado pelo grafo).
    inputs = {"messages": [{"role": "user", "content": user_text}]}
    # Aqui usamos .stream para demonstrar, mas podemos usar .run dependendo da sua versão.
    # Vamos coletar a última atualização dos chunks e retornar um texto.
    try:
        last_text = None
        for mode, chunk in agent.stream(inputs, stream_mode="updates"):
            # Normalmente os chunks são updates de estado; a saída final de texto costuma vir como 'messages' ou 'assistant' output.
            # Para simplificar, tentamos extrair um texto amigável do chunk.
            if isinstance(chunk, dict):
                # procura por mensagens ou resultados legíveis
                # Este trecho é defensivo: formato exato pode variar entre versões, ajuste conforme sua versão do LangGraph.
                if "messages" in chunk:
                    msgs = chunk["messages"]
                    if msgs and isinstance(msgs, list):
                        last_text = msgs[-1].get("content") or last_text
                elif "assistant" in chunk:
                    last_text = chunk["assistant"].get("content") or last_text
                else:
                    # fallback: stringify chunk
                    last_text = str(chunk)
            else:
                last_text = str(chunk)
        return last_text or "Desculpe, não obtive resposta do agente."
    except Exception as e:
        # Em alguns setups, agent.run/agent.stream pode diferir; capture o erro e retorne message.
        return f"Erro ao executar agente: {str(e)}"

# ---------- CLI simples para teste ----------
if __name__ == "__main__":
    print("Chat LangGraph (exemplo). Escreva 'sair' para encerrar.")
    while True:
        user = input("\nVocê: ").strip()
        if not user:
            continue
        if user.lower() in ("sair", "exit", "quit"):
            break
        resp = handle_user_message(user)
        print("\nAssistente:\n" + resp)
