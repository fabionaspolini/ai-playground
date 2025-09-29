"""
Exemplo mínimo de uso de RunnableWithMessageHistory (LangChain) em Python.
- Usa InMemoryChatMessageHistory para persistir histórico por `session_id`.
- Envia mensagens para ChatOpenAI (requere `OPENAI_API_KEY`).

Como usar:
1) pip install -U langchain-core langchain-openai openai
2) export OPENAI_API_KEY="sua_chave"
3) python exemplo_langchain_runnable_with_history.py

Observação: este é um exemplo didático. Em produção troque InMemoryChatMessageHistory
por uma implementação persistente (Redis, Postgres, etc.).
"""

import os
from typing import Dict

from langchain_core.runnables import RunnableConfig
# Model / integração OpenAI
from langchain_openai import ChatOpenAI

# Prompts e mensagens
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage

# Histórico de chat (in-memory para exemplo)
from langchain_core.chat_history import InMemoryChatMessageHistory

# Runnable com suporte a histórico
from langchain_core.runnables.history import RunnableWithMessageHistory

# ---------- Configurações ----------
MODEL_NAME = "openai/gpt-oss-20b" # os.environ.get("LLM_MODEL", "gpt-4o-mini")

# ---------- Prompt (inclui placeholder para histórico) ----------
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "Você é um assistente útil. Responda brevemente."),
        MessagesPlaceholder("history"),
        ("human", "{input}"),
    ]
)

# ---------- Runnable (prompt |> modelo) ----------
# O operador '|' compõe runnables (prompt -> modelo)
llm = ChatOpenAI(model=MODEL_NAME, temperature=0.0, base_url="http://localhost:1234/v1")
chain = prompt | llm

# ---------- Fábrica de histórico baseada em session_id (store simples) ----------
_store: Dict[str, InMemoryChatMessageHistory] = {}

def get_history_by_session_id(session_id: str) -> InMemoryChatMessageHistory:
    """Retorna (ou cria) um histórico para a session_id informada."""
    if session_id not in _store:
        _store[session_id] = InMemoryChatMessageHistory()
    return _store[session_id]

# ---------- Envolvendo a chain com RunnableWithMessageHistory ----------
with_history = RunnableWithMessageHistory(
    chain,
    get_history_by_session_id,
    # Como o prompt usa {input} como texto do usuário, indicamos input_messages_key="input"
    input_messages_key="input",
    # O placeholder no prompt chama-se "history"
    history_messages_key="history",
)

# ---------- Função utilitária para conversar por sessão ----------

def send_message(session_id: str, user_text: str):
    """Envia uma mensagem para a chain com histórico e retorna a resposta."""
    print("============= SEND MESSAGE =============")
    print(f"[session_id={session_id}] Você: {user_text}")
    response = with_history.invoke(
        {"input": user_text},
        config=RunnableConfig(configurable={"session_id": session_id}),
    )
    # A resposta pode vir como string ou BaseMessage dependendo do runnable
    # Normalmente ChatOpenAI retorna uma string tratável como AI message
    print("Resposta crua do Runnable:", response)

    # Para inspecionar o histórico salvo:
    history = get_history_by_session_id(session_id)
    print("--- Histórico armazenado (mensagens) ---")
    for m in history.messages:
        who = "human" if m.type == "human" else "ai" if m.type == "ai" else "other"
        print(f"[{who}] {m.content}")
    print("---------------------------------------\n")

    return response


# ---------- Pequeno loop de demonstração ----------
if __name__ == "__main__":
    sess = "demo-session-1"
    print("Exemplo RunnableWithMessageHistory - sessão:", sess)

    send_message(sess, "Olá, qual é a capital do Brasil?")
    send_message(sess, "e de Santa Catarina?")
    send_message(sess, "e do Paraná?")
    send_message(sess, "Resuma em uma frase as respostas anteriores.")

    # Exemplo com outra sessão (isola histórico)
    sess2 = "outra-sessao"
    send_message(sess2, "Me diga uma curiosidade sobre cachorros.")

    print("Fim do exemplo. \nPara produção: troque InMemoryChatMessageHistory por um backend persistente.")
