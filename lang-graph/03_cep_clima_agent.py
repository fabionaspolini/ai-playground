from typing import List, TypedDict

import requests
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph

# Config for LM Studio
llm = ChatOpenAI(
    base_url="http://localhost:1234/v1",
    model="openai/gpt-oss-20b",
    temperature=0.7
)

# Types for our state
class AgentState(TypedDict):
    messages: List[dict]
    current_step: str

# CEP Agent
def get_address_from_cep(cep: str) -> dict:
    """Get address details from a CEP using viacep.com.br"""
    cep = cep.replace("-", "").replace(".", "").strip()
    url = f"https://viacep.com.br/ws/{cep}/json/"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return {"error": "CEP não encontrado"}

def cep_agent(state: AgentState) -> AgentState:
    """Agent that handles CEP queries"""
    last_message = state["messages"][-1]["content"].lower()
    
    # Check if message contains CEP
    if "cep" in last_message:
        # Extract CEP using LLM
        prompt = ChatPromptTemplate.from_messages([
            # ("system", "Extract the CEP number from the message. Return only the CEP number, nothing else."),
            ("system", "Extraia o número do CEP da mensagem. Retorne apenas o número do CEP, nada mais."),
            ("human", last_message)
        ])
        cep_chain = prompt | llm
        cep_response = cep_chain.invoke({})
        cep = cep_response.content.strip()
        # cep = llm.invoke(prompt).content.strip()
        
        # Get address info
        address_info = get_address_from_cep(cep)
        
        if "error" not in address_info:
            response = f"Endereço para o CEP {cep}:\n"
            response += f"Logradouro: {address_info.get('logradouro', 'N/A')}\n"
            response += f"Bairro: {address_info.get('bairro', 'N/A')}\n"
            response += f"Cidade: {address_info.get('localidade', 'N/A')}\n"
            response += f"Estado: {address_info.get('uf', 'N/A')}"
        else:
            response = "Desculpe, não foi possível encontrar informações para este CEP."
            
        state["messages"].append({"role": "assistant", "content": response})
        state["current_step"] = "end"
    else:
        state["current_step"] = "weather_agent"
        
    return state

# Weather Agent (Mock)
def weather_agent(state: AgentState) -> AgentState:
    """Agent that handles weather queries"""
    last_message = state["messages"][-1]["content"].lower()
    
    # Check if message is about weather
    if any(word in last_message for word in ["clima", "temperatura", "tempo"]):
        # Mock response - this will be replaced with actual weather API implementation
        response = "Mock da previsão do tempo: \n"
        response += "Temperatura: 25°C\n"
        response += "Condição: Ensolarado\n"
        response += "Umidade: 65%"
        
        state["messages"].append({"role": "assistant", "content": response})
        state["current_step"] = "end"
    else:
        state["current_step"] = "general_chat"
        
    return state

# General Chat Agent
def general_chat_agent(state: AgentState) -> AgentState:
    """Agent that handles general conversation"""
    messages = state["messages"]
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", """Você é um assistente amigável e prestativo. 
        Você pode responder perguntas gerais e conversar naturalmente.
        Mantenha as respostas concisas e relevantes."""),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}")
    ])
    
    # Format message history
    history = []
    for msg in messages[:-1]:  # Exclude the last message
        if msg["role"] == "user":
            history.append(HumanMessage(content=msg["content"]))
        else:
            history.append(AIMessage(content=msg["content"]))
            
    response = llm.invoke(
        prompt.format_messages(
            history=history,
            input=messages[-1]["content"]
        )
    )
    
    state["messages"].append({"role": "assistant", "content": response.content})
    state["current_step"] = "end"
    return state

# Create the graph
workflow = StateGraph(AgentState)

# Add nodes
workflow.add_node("cep_agent", cep_agent)
workflow.add_node("weather_agent", weather_agent)
workflow.add_node("general_chat", general_chat_agent)

# Add edges
workflow.add_edge("cep_agent", "weather_agent")
workflow.add_edge("weather_agent", "general_chat")

# Set entry point
workflow.set_entry_point("cep_agent")

# Compile the graph
graph = workflow.compile()
graph.get_graph().draw_mermaid_png(output_file_path="03_cep_clima_agent.png")

# Chat function
def chat(message: str, history: List[dict] = None) -> str:
    """Main chat function"""
    print(f"User: {message}")
    
    if history is None:
        history = []
        
    # Add user message to history
    history.append({"role": "user", "content": message})
    
    # Run the graph
    result = graph.invoke({
        "messages": history,
        "current_step": "cep_agent"
    })
    
    # Return the last assistant message
    chat_response = result["messages"][-1]["content"]
    print("Assistant:", chat_response)
    return chat_response

# Example usage
if __name__ == "__main__":
    # response = chat("Qual o endereço do CEP 01311-000?")
    # response = chat("Qual o clima em São Paulo, SP?")
    # response = chat("Qual capital do Brasil")

    # Testar query com dois agents
    response = chat("Qual o clima no CEP 01311-000?")
    
