from typing import TypedDict, Sequence

import requests
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.graph import StateGraph, END
from langgraph.graph.state import CompiledStateGraph


# Define os tipos para o estado do graph
class AgentState(TypedDict):
    messages: Sequence[HumanMessage | AIMessage]
    current_cep: str | None

# Função para extrair CEP da mensagem do usuário
def extract_cep(state: AgentState):
    messages = state["messages"]
    last_message = messages[-1].content
    
    cep = ''.join(filter(str.isdigit, last_message))
    # state.current_cep = cep
    return {"current_cep": cep}

# Função para consultar o CEP na API ViaCEP
def query_cep(state: AgentState):
    cep = state["current_cep"]
    if not cep:
        return {
            "messages": [
                *state["messages"],
                AIMessage(content="Não identifiquei um CEP válido na sua mensagem. Por favor, forneça um CEP no formato XXXXX-XXX.")
            ]
        }
    
    try:
        response = requests.get(f"https://viacep.com.br/ws/{cep}/json/")
        data = response.json()
        
        if "erro" in data:
            return {
                "messages": [
                    *state["messages"],
                    AIMessage(content="CEP não encontrado. Por favor, verifique se o CEP está correto.")
                ]
            }
        
        # Formata a resposta com os dados do CEP
        address_info = (
            f"📍 Informações do CEP {cep}:\n"
            f"Logradouro: {data.get('logradouro', 'N/A')}\n"
            f"Bairro: {data.get('bairro', 'N/A')}\n"
            f"Cidade: {data.get('localidade', 'N/A')}\n"
            f"Estado: {data.get('uf', 'N/A')}\n"
            f"CEP: {data.get('cep', 'N/A')}"
        )
        
        return {
            "messages": [
                *state["messages"],
                AIMessage(content=address_info)
            ]
        }
    except Exception as e:
        return {
            "messages": [
                *state["messages"],
                AIMessage(content="Desculpe, ocorreu um erro ao consultar o CEP. Por favor, tente novamente.")
            ]
        }

# Configuração do graph
def configure_graph() -> CompiledStateGraph:
    # Define o estado inicial
    workflow = StateGraph(AgentState)
    
    # Adiciona os nós
    workflow.add_node("extract_cep", extract_cep)
    workflow.add_node("query_cep", query_cep)
    
    # Conecta os nós
    workflow.add_edge("extract_cep", "query_cep")
    workflow.add_edge("query_cep", END)
    
    # Define o ponto de entrada
    workflow.set_entry_point("extract_cep")
    
    # Compila o graph
    chain = workflow.compile()
    
    return chain

# Função principal para processar mensagens
def process_message(message: str, chain: CompiledStateGraph):
    state: AgentState = {
        "messages": [HumanMessage(content=message)],
        "current_cep": None
    }
    
    result = chain.invoke(state)
    return result["messages"][-1].content

def main():
    chain = configure_graph()
    print("🤖 Assistente de CEP iniciado! Digite 'sair' para encerrar.")
    print("Por favor, digite um CEP para consulta (formato: XXXXX-XXX):")
    
    while True:
        user_input = input("\nVocê: ")
        if user_input.lower() == 'sair':
            print("Até logo! 👋")
            break
            
        response = process_message(user_input, chain)
        print(f"\nAssistente: {response}")

if __name__ == "__main__":
    main()
