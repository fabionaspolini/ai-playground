"""
Exemplo com RunnableWithMessageHistory e sumarização recursiva do histórico.
- A cada 20 mensagens, sumariza as 10 mais antigas e substitui por um resumo (5 do usuário + 5 do assistente).
- Mantém as outras 10 mensagens mais recentes do histórico para detalhes.

Como usar:
1) pip install -U langchain-core langchain-openai openai
2) export OPENAI_API_KEY="sua_chave"
3) python exemplo_langchain_runnable_with_history.py
"""

import os
from typing import Dict, List

from langchain_core.runnables import RunnableConfig
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage, SystemMessage
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

# ---------- Configurações ----------
MODEL_NAME = "openai/gpt-oss-20b"  # os.environ.get("LLM_MODEL", "gpt-4o-mini")

SUMARIZE_AFTER_MESSAGES = 20  # número total de mensagens (10 usuário + 10 assistente) para acionar sumarização
MESSAGES_TO_SUMMARIZE = 10  # número de mensagens mais antigas a serem resumidas (5 usuário + 5 assistente)

# ---------- Prompt base ----------
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "Você é um assistente de conversa para uma aplicação que simula em chat com Gen AI."),
        MessagesPlaceholder("history"),
        ("human", "{input}"),
    ]
)

llm = ChatOpenAI(model=MODEL_NAME, temperature=0.0, base_url="http://localhost:1234/v1")
chain = prompt | llm

_store: Dict[str, InMemoryChatMessageHistory] = {}


def get_history_by_session_id(session_id: str) -> InMemoryChatMessageHistory:
    if session_id not in _store:
        _store[session_id] = InMemoryChatMessageHistory()
    return _store[session_id]


with_history = RunnableWithMessageHistory(
    chain,
    get_history_by_session_id,
    input_messages_key="input",
    history_messages_key="history",
)


# ---------- Função de sumarização ----------

def summarize_messages(messages: List[BaseMessage]) -> str:
    """Gera um resumo textual das mensagens fornecidas."""
    text_parts = []
    for m in messages:
        who = "user" if isinstance(m, HumanMessage) else "assistant"
        text_parts.append(f"{who}: {m.content}")

    join_text = "\n".join(text_parts)
    summary_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "Você está sendo utilizado para comprimir a parte inicial das mensagens de um chat.\n" \
                       "Você deve resumir o texto, mas preservar detalhes importantes, como nomes, datas, fatos.\n" \
                       "O objetivo é utilizar esse resumo para manter o contexto da conversa, mas economizar tokens.\n" \
                       "Preserve o idioma original do texto."),
            ("human", join_text),
        ]
    )
    summary_chain = summary_prompt | llm
    summary = summary_chain.invoke({})
    return summary.content if isinstance(summary, AIMessage) else str(summary)


# ---------- Controle recursivo de histórico ----------

def maybe_summarize_history(session_id: str):
    history = get_history_by_session_id(session_id)
    messages = history.messages

    if len(messages) >= SUMARIZE_AFTER_MESSAGES:
        # Pega as 10 mais antigas para resumir (5 do usuário + 5 do assistente)
        to_summarize = messages[:MESSAGES_TO_SUMMARIZE]
        summary_text = summarize_messages(to_summarize)

        # Substitui por uma mensagem "resumo"
        new_messages: list[BaseMessage] = [
            AIMessage(content=f"Resumo compactado da conversa inicial para economia de tokens:\n{summary_text}")]
        new_messages.extend(messages[MESSAGES_TO_SUMMARIZE:])  # mantém as 10 mais recentes

        # Atualiza histórico
        history.clear()
        for m in new_messages:
            history.add_message(m)


# ---------- Função utilitária de envio ----------

def send_message(session_id: str, user_text: str):
    print("============= SEND MESSAGE =============")
    print(f"[session_id={session_id}] Você: {user_text}")

    # Antes de cada interação, checa se é hora de resumir
    maybe_summarize_history(session_id)

    # Envia a mensagem e obtém a resposta
    response = with_history.invoke(
        {"input": user_text},
        config=RunnableConfig(configurable={"session_id": session_id}),
    )

    history = get_history_by_session_id(session_id)
    print("--- Histórico armazenado ---")
    for m in history.messages:
        who = m.type
        print(f"[{who}] {m.content}")
    print("----------------------------\n")

    return response


if __name__ == "__main__":
    sess = "demo-session-1"
    print("Exemplo com sumarização recursiva do histórico:", sess)

    send_message(sess, "Qual capital do Brasil?")  # 1
    send_message(sess, "e de Santa Catarina?")  # 2
    send_message(sess, "e do Paraná?")  # 3
    send_message(sess, "e do Rio Grande do Sul?")  # 4
    send_message(sess, "e de São Paulo?")  # 5 - Ao enviar a mensagem #11, será resumido o histórico até aqui.
    send_message(sess, "e do Rio de Janeiro?")  # 6
    send_message(sess, "e de Minas Gerais?")  # 7
    send_message(sess, "e do Espírito Santo?")  # 8
    send_message(sess, "e do Mato Grosso?")  # 9
    send_message(sess, "e do Mato Grosso do Sul?")  # 10 - Ao enviar a mensagem #16, será resumido o histórico até aqui.
    send_message(sess, "e do Goiás?")  # 11 - aqui deve resumir as 10 primeiras mensagens (pergunta e resposta até passo #5).
    send_message(sess, "e da Bahia?")  # 12
    send_message(sess, "e de Pernambuco?")  # 13
    send_message(sess, "e do Ceará?")  # 14
    send_message(sess, "e do Rio Grande do Norte?")  # 15
    send_message(sess, "e da Paraíba?")  # 16 - aqui deve resumir
    send_message(sess, "e do Amazonas?")  # 17
    send_message(sess, "Resuma em uma frase as respostas anteriores.")  # 18

    print("Fim do exemplo.")
