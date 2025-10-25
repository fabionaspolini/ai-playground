from typing import Annotated, Sequence, TypedDict, Union
from langgraph.graph import StateGraph, END
import json
import requests
from openai import OpenAI

# Configuração do cliente OpenAI
client = OpenAI()

# Tipos de mensagens
class Message(TypedDict):
    content: str
    role: str

# Estado do grafo
class State(TypedDict):
    messages: Sequence[Message]
    current_step: str

# Função para consultar CEP
def consultar_cep(cep):
    try:
        url = f'https://viacep.com.br/ws/{cep}/json/'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if 'erro' not in data:
                return data
    except Exception as e:
        return None
    return None

# Função para obter clima (mock)
def obter_clima(cidade, estado):
    # Mockando resposta do clima
    return {
        "cidade": cidade,
        "estado": estado,
        "temperatura": "25°C",
        "condicao": "Ensolarado",
        "umidade": "65%"
    }

# Agente de CEP
def agente_cep(state: State):
    messages = state["messages"]
    last_message = messages[-1]["content"].lower()
    
    if "cep" in last_message:
        try:
            # Extrai o CEP da mensagem (assumindo formato XXXXX-XXX ou XXXXXXXX)
            import re
            cep = re.findall(r'\d{5}-?\d{3}', last_message)[0]
            cep = cep.replace("-", "")
            
            endereco = consultar_cep(cep)
            if endereco:
                response = f"Endereço encontrado:\nLogradouro: {endereco.get('logradouro', 'N/A')}\n" \
                          f"Bairro: {endereco.get('bairro', 'N/A')}\n" \
                          f"Cidade: {endereco.get('localidade', 'N/A')}\n" \
                          f"Estado: {endereco.get('uf', 'N/A')}"
                return {"messages": [*messages, {"role": "assistant", "content": response}]}
            else:
                return {"messages": [*messages, {"role": "assistant", "content": "CEP não encontrado."}]}
        except:
            return {"messages": messages}
    return {"messages": messages}

# Agente de Clima
def agente_clima(state: State):
    messages = state["messages"]
    last_message = messages[-1]["content"].lower()
    
    # Verifica se é uma consulta de clima por cidade/estado
    if "clima" in last_message and "cep" not in last_message:
        try:
            # Análise básica para extrair cidade e estado
            prompt = f"""
            Extraia a cidade e o estado da seguinte mensagem: '{last_message}'
            Retorne apenas um JSON no formato: {{"cidade": "nome_cidade", "estado": "UF"}}
            """
            
            completion = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                response_format={ "type": "json_object" }
            )
            
            resultado = json.loads(completion.choices[0].message.content)
            clima = obter_clima(resultado["cidade"], resultado["estado"])
            
            response = f"Clima em {clima['cidade']}/{clima['estado']}:\n" \
                      f"Temperatura: {clima['temperatura']}\n" \
                      f"Condição: {clima['condicao']}\n" \
                      f"Umidade: {clima['umidade']}"
            
            return {"messages": [*messages, {"role": "assistant", "content": response}]}
        except:
            return {"messages": messages}
    return {"messages": messages}

# Agente de Clima por CEP
def agente_clima_cep(state: State):
    messages = state["messages"]
    last_message = messages[-1]["content"].lower()
    
    if "clima" in last_message and "cep" in last_message:
        try:
            # Extrai o CEP
            import re
            cep = re.findall(r'\d{5}-?\d{3}', last_message)[0]
            cep = cep.replace("-", "")
            
            # Consulta o endereço
            endereco = consultar_cep(cep)
            if endereco:
                # Obtém o clima da cidade encontrada
                clima = obter_clima(endereco['localidade'], endereco['uf'])
                
                response = f"Clima em {clima['cidade']}/{clima['estado']}:\n" \
                          f"Temperatura: {clima['temperatura']}\n" \
                          f"Condição: {clima['condicao']}\n" \
                          f"Umidade: {clima['umidade']}"
                
                return {"messages": [*messages, {"role": "assistant", "content": response}]}
            else:
                return {"messages": [*messages, {"role": "assistant", "content": "CEP não encontrado."}]}
        except:
            return {"messages": messages}
    return {"messages": messages}

# Função para determinar o próximo passo
def router(state: State) -> str:
    messages = state["messages"]
    last_message = messages[-1]["content"].lower()
    
    if "clima" in last_message and "cep" in last_message:
        return "clima_cep"
    elif "clima" in last_message:
        return "clima"
    elif "cep" in last_message:
        return "cep"
    return END

# Configuração do grafo
workflow = StateGraph(State)

# Adiciona os nós ao grafo
workflow.add_node("router", router)
workflow.add_node("cep", agente_cep)
workflow.add_node("clima", agente_clima)
workflow.add_node("clima_cep", agente_clima_cep)

# Configura as arestas do grafo
workflow.set_entry_point("router")
workflow.add_conditional_edges(
    "router",
    router,
    {
        "cep": "cep",
        "clima": "clima",
        "clima_cep": "clima_cep",
        END: END
    }
)

workflow.add_edge("cep", "router")
workflow.add_edge("clima", "router")
workflow.add_edge("clima_cep", "router")

# Compila o grafo
app = workflow.compile()

app.get_graph().draw_mermaid_png(output_file_path="99_agente_02.png")

# Função para processar mensagens
def process_message(message: str) -> str:
    response = app.invoke({
        "messages": [{"role": "user", "content": message}],
        "current_step": "router"
    })
    return response["messages"][-1]["content"]

# Exemplo de uso
if __name__ == "__main__":
    # Teste de consulta de CEP
    print("Teste 1: Consulta de CEP")
    response = process_message("Qual o endereço do CEP 01311-000?")
    print(response)
    print("\n")

    # Teste de consulta de clima
    print("Teste 2: Consulta de clima por cidade")
    response = process_message("Qual o clima em São Paulo, SP?")
    print(response)
    print("\n")

    # Teste de consulta de clima por CEP
    print("Teste 3: Consulta de clima por CEP")
    response = process_message("Qual o clima no CEP 01311-000?")
    print(response)
