from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from typing import TypedDict, Literal
import requests

# -----------------------------
# Estado do Grafo
# -----------------------------
class ChatState(TypedDict):
    user_input: str
    output: str
    action: Literal["cep", "clima", "clima_por_cep", "done"]


# -----------------------------
# Agente 1: Resolver CEP
# -----------------------------
def agente_cep(state: ChatState):
    cep = ''.join(filter(str.isdigit, state["user_input"]))
    url = f"https://viacep.com.br/ws/{cep}/json/"
    try:
        resp = requests.get(url, timeout=5).json()
        if "erro" in resp:
            return {"output": f"CEP {cep} não encontrado.", "action": "done"}
        cidade = resp.get("localidade")
        estado = resp.get("uf")
        return {
            "output": f"Endereço do CEP {cep}: {resp.get('logradouro')}, {cidade} - {estado}",
            "cidade": cidade,
            "estado": estado,
            "action": "done",
        }
    except Exception as e:
        return {"output": f"Erro consultando CEP: {str(e)}", "action": "done"}


# -----------------------------
# Agente 2: Resolver Clima
# -----------------------------
def agente_clima(state: ChatState):
    # Mockado - aqui você substituiria por um serviço real
    if "cidade" in state and "estado" in state:
        cidade, estado = state["cidade"], state["estado"]
    else:
        partes = state["user_input"].split()
        cidade, estado = partes[0], partes[-1]

    clima = f"O clima em {cidade}-{estado} é ensolarado, 28°C (mockado)."
    return {"output": clima, "action": "done"}


# -----------------------------
# Supervisor: Decide ação
# -----------------------------
def supervisor(state: ChatState):
    texto = state["user_input"].lower()

    if "cep" in texto and "clima" in texto:
        return {"action": "clima_por_cep"}
    elif any(p in texto for p in ["cep", "endereço"]):
        return {"action": "cep"}
    elif "clima" in texto:
        return {"action": "clima"}
    else:
        return {"output": "Não entendi sua solicitação.", "action": "done"}


# -----------------------------
# Grafo Principal
# -----------------------------
graph = StateGraph(ChatState)

graph.add_node("supervisor", supervisor)
graph.add_node("cep", agente_cep)
graph.add_node("clima", agente_clima)

# Fluxos
graph.add_edge("supervisor", "cep", condition=lambda s: s["action"] == "cep")
graph.add_edge("supervisor", "clima", condition=lambda s: s["action"] == "clima")
graph.add_conditional_edges(
    "supervisor",
    lambda s: s["action"],
    {
        "clima_por_cep": "cep",
        "done": END,
    },
)
# Se pediu clima_por_cep → CEP → Clima
graph.add_edge("cep", "clima", condition=lambda s: s.get("action") == "clima_por_cep")

graph.set_entry_point("supervisor")

# Checkpointer para manter contexto
memory = MemorySaver()
app = graph.compile(checkpointer=memory)

app.get_graph().draw_mermaid_png(output_file_path="99_agente.png")


# -----------------------------
# Exemplo de uso
# -----------------------------
if __name__ == "__main__":
    perguntas = [
        "Qual o endereço do CEP 01001000?",
        "Qual o clima em Florianópolis SC?",
        "Qual o clima no CEP 01001000?",
        "Me diga o clima agora",
    ]

    for pergunta in perguntas:
        print(f"\nUsuário: {pergunta}")
        resposta = app.invoke({"user_input": pergunta, "action": None, "output": ""})
        print("Assistente:", resposta["output"])
