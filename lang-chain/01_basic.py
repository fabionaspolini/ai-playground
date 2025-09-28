"""
app_langchain_chat_memoria.py
Uma aplicação simples em Python usando LangChain (ConversationChain + memória) para aprender a criar um chat com histórico.

O que faz: roda um loop de terminal onde você conversa livremente com o modelo. O histórico da conversa é lembrado e usado para as próximas respostas.

Tipos de memória suportados (você pode trocar no código):
 - ConversationBufferMemory: armazena toda a conversa.
 - ConversationSummaryMemory: mantém um resumo do histórico para economizar tokens.
 - ConversationBufferWindowMemory: mantém apenas as últimas N interações.

Requisitos:
  - Python 3.10+
  - pip install langchain langchain-openai openai python-dotenv

Como usar:
 1. crie um arquivo .env com a variável OPENAI_API_KEY (ou exporte a variável de ambiente):
    OPENAI_API_KEY=sk-...
 2. instale dependências: pip install langchain langchain-openai openai python-dotenv
 3. rode: python app_langchain_chat_memoria.py

Observação: escolha o modelo que quiser via parâmetro `model` do ChatOpenAI. Se usar uma conta OpenAI gratuita, prefira `gpt-3.5-turbo`.

"""

import os
from dotenv import load_dotenv

# Carrega variável OPENAI_API_KEY do .env (se existir)
load_dotenv()

# Importações do LangChain
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory, ConversationSummaryMemory, ConversationBufferWindowMemory


def criar_conversation_chain(
        model_name: str | None = None,
        temperature: float = 0.7,
        memory_type: str = "buffer",
) -> ConversationChain:
    """Cria e retorna uma ConversationChain com memória configurável.

    memory_type pode ser:
      - "buffer"   -> guarda toda a conversa
      - "summary"  -> guarda um resumo
      - "window"   -> guarda apenas as últimas N trocas
    """

    # Inicializa o LLM
    if model_name:
        llm = ChatOpenAI(model=model_name, temperature=temperature, openai_api_base="http://localhost:1234/v1")
    else:
        llm = ChatOpenAI(temperature=temperature, openai_api_base="http://localhost:1234/v1",)

    # Seleciona tipo de memória
    if memory_type == "summary":
        memory = ConversationSummaryMemory(llm=llm, return_messages=True)
    elif memory_type == "window":
        memory = ConversationBufferWindowMemory(k=3, return_messages=True)
    else:
        memory = ConversationBufferMemory(return_messages=True)

    # Cria a chain de conversação
    chain = ConversationChain(
        llm=llm,
        memory=memory,
        verbose=True  # mostra logs internos (pode desligar)
    )
    return chain


def main():
    print("Aplicação LangChain — chat com memória (buffer/summary/window)\n(entre 'sair' para terminar)\n")

    # Permite sobrescrever o modelo e tipo de memória via variáveis de ambiente
    model = os.environ.get("LANGCHAIN_MODEL")
    memory_type = os.environ.get("LANGCHAIN_MEMORY", "buffer")  # default: buffer

    chain = criar_conversation_chain(model_name=model, temperature=0.7, memory_type=memory_type)

    while True:
        texto = input("Você: ")
        if not texto:
            continue
        if texto.strip().lower() in ("sair", "quit", "exit"):
            print("Tchau!")
            break

        # Executa a chain com memória
        try:
            resposta = chain.predict(input=texto)
            print("Assistente:", resposta.strip())
        except Exception as e:
            print("Erro ao chamar o LLM:", e)
            print("Verifique sua OPENAI_API_KEY e se as dependências estão instaladas.")


if __name__ == "__main__":
    main()
