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
        if hasattr(m, "is_resume") and m.is_resume:
            # content_without_first_line = "\n".join(m.content.split("\n")[1:]).strip()
            text_parts.append(f"### Resumo de conversa anterior\n\n{m.content}\n")
            text_parts.append("### Fim do resumo e começo de novas mensagens para agregar ao resumo anterior\n\n")
        else:
            
            who = "user" if isinstance(m, HumanMessage) else "assistant"
            text_parts.append(f"{who}: {m.content}")

    join_text = "\n".join(text_parts)
    summary_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "Você está sendo utilizado para comprimir a parte inicial das mensagens de um chat.\n"
                       "Você deve resumir o texto, mas preservar detalhes importantes, como nomes, datas, fatos.\n"
                       "O objetivo é utilizar esse resumo para manter o contexto da conversa, mas economizar tokens.\n\n"
                       "**Regras**:\n" \
                       "- Preserve o idioma original do texto.\n"
                       f"- A cada {SUMARIZE_AFTER_MESSAGES} mensagens, são compactadas as {MESSAGES_TO_SUMMARIZE} mais antigas em um resumo.\n"
                       f"- Você pode estar resumindo novas mensagens, e um resumo anterior já existente. O resultado deve agregar ambos em um novo resumo.\n"
                       f"- Sua resposta não precisa citar que é um resumo, apenas gere o conteúdo."),
            ("human", join_text),
        ]
    )
    summary_chain = summary_prompt | llm
    summary = summary_chain.invoke({})
    return summary.content if isinstance(summary, AIMessage) else str(summary)


# ---------- Controle recursivo de histórico ----------

def _count_user_or_ai_messages(messages: List[BaseMessage]) -> int:
    count = 0
    for m in messages:
        if isinstance(m, (HumanMessage, AIMessage)):
            count += 1
    return count

def _count_start_ai_messages(messages: List[BaseMessage]) -> int:
    count = 0
    for m in messages:
        if isinstance(m, AIMessage):
            count += 1
        else:
            break
    return count

def maybe_summarize_history(session_id: str):
    history = get_history_by_session_id(session_id)
    messages = history.messages

    if _count_user_or_ai_messages(messages) >= SUMARIZE_AFTER_MESSAGES:
        start_ai_messages_count = _count_start_ai_messages(messages)
        
        # Pega as 10 mais antigas para resumir (5 do usuário + 5 do assistente)
        to_summarize = messages[:(start_ai_messages_count + MESSAGES_TO_SUMMARIZE)]
        summary_text = summarize_messages(to_summarize)

        # Substitui por uma mensagem "resumo"
        new_messages: list[BaseMessage] = [
            AIMessage(content=f"Essa mensagem é um resumo para compactar mensagens anteriores e economizar tokens, "
                              f"mas preservar contexto da conversa:\n{summary_text}", is_resume=True)]
        new_messages.extend(messages[(start_ai_messages_count + MESSAGES_TO_SUMMARIZE):])  # mantém as 10 mais recentes

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
    send_message(sess, "Quantas capitais você me falou até agora?")  # 18 - 17 capitais (1 nacional + 16 estaduais)
    send_message(sess, "Resuma em uma frase as respostas anteriores.")  # 19

    print("Fim do exemplo.")

    ### ULTIMA RESPOSTA ###
    # --- Histórico armazenado ---
    # [ai] Essa mensagem é um resumo para compactar mensagens anteriores e economizar tokens, mas preservar contexto da conversa:
    # Capital do Brasil: Brasília
    # Capitais dos estados citados:
    # - Santa Catarina: Florianópolis
    # - Paraná: Curitiba
    # - Rio Grande do Sul: Porto Alegre
    # - São Paulo: São Paulo (cidade que dá nome ao estado)
    # - Rio de Janeiro: Rio de Janeiro
    # - Minas Gerais: Belo Horizonte
    # - Espírito Santo: Vitória
    # - Mato Grosso: Cuiabá
    # - Mato Grosso do Sul: Campo Grande
    # [human] e do Goiás?
    # [ai] A capital do estado de Goiás é **Goiânia**.
    # [human] e da Bahia?
    # [ai] A capital do estado da Bahia é **Salvador**.
    # [human] e de Pernambuco?
    # [ai] A capital do estado de Pernambuco é **Recife**.
    # [human] e do Ceará?
    # [ai] A capital do estado do Ceará é **Fortaleza**.
    # [human] e do Rio Grande do Norte?
    # [ai] A capital do estado do Rio Grande do Norte é **Natal**.
    # [human] e da Paraíba?
    # [ai] A capital do estado da Paraíba é **João Pessoa**.
    # [human] e do Amazonas?
    # [ai] A capital do estado do Amazonas é **Manaus**.
    # [human] Quantas capitais você me falou até agora?
    # [ai] Você recebeu **17** capitais até agora.
    # [human] Resuma em uma frase as respostas anteriores.
    # [ai] Até agora eu citei as capitais brasileiras: Brasília; Florianópolis (SC), Curitiba (PR), Porto Alegre (RS), São Paulo (SP), Rio de Janeiro (RJ), Belo Horizonte (MG), Vitória (ES), Cuiabá (MT), Campo Grande (MS), Goiânia (GO), Salvador (BA), Recife (PE), Fortaleza (CE), Natal (RN), João Pessoa (PB) e Manaus (AM).
    # ----------------------------
