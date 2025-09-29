"""
Aplicação com memória customizada.

A cada 10 mensagens, são sumarizadas as 5 mais antigas, mantendo um resumo
da conversa. Assim, o histórico não cresce indefinidamente.
"""

import os
from typing import List

from dotenv import load_dotenv
from langchain.memory.chat_memory import BaseChatMemory
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage

# Carrega variável OPENAI_API_KEY do .env (se existir)
load_dotenv()

# Importações do LangChain
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory, ConversationSummaryMemory, ConversationBufferWindowMemory

class RecursiveSummarizerMemory(BaseChatMemory):
    def __init__(self, llm: ChatOpenAI, window_size: int = 5, summarize_every: int = 10):
        super().__init__()
        self.window_size = window_size
        self.llm = llm
        self.summarize_every = summarize_every
        self.buffer: List[BaseMessage] = []
        self.summary: str = ""   # resumo acumulado
        self.message_count = 0

    @property
    def memory_variables(self) -> List[str]:
        return ["history"]

    def load_memory_variables(self, inputs):
        """Retorna o histórico como resumo + mensagens recentes"""
        text_history = ""
        if self.summary:
            text_history += f"Resumo acumulado:\n{self.summary}\n\n"
        if self.buffer:
            text_history += "Mensagens recentes:\n"
            for msg in self.buffer:
                role = "Usuário" if isinstance(msg, HumanMessage) else "Assistente"
                text_history += f"{role}: {msg.content}\n"
        return {"history": text_history}

    def save_context(self, inputs, outputs) -> None:
        """Salva as novas mensagens no buffer e resume quando necessário"""
        self.buffer.append(HumanMessage(content=inputs["input"]))
        self.buffer.append(AIMessage(content=outputs["response"]))
        self.message_count += 1

        # quando chegar ao limite de mensagens
        if self.message_count >= self.summarize_every:
            self._summarize_oldest()
            self.message_count = 0

    def _summarize_oldest(self):
        """Resume as N mensagens mais antigas e atualiza o resumo acumulado"""
        if len(self.buffer) <= self.window_size:
            return

        # separa as 5 mensagens mais antigas
        oldest = self.buffer[:self.window_size]
        self.buffer = self.buffer[self.window_size:]  # remove elas do buffer

        text_to_summarize = "\n".join(
            [f"Usuário: {msg.content}" if isinstance(msg, HumanMessage) else f"Assistente: {msg.content}"
             for msg in oldest]
        )

        prompt = f"Resuma de forma concisa o seguinte trecho da conversa:\n{text_to_summarize}\n\nResumo anterior:\n{self.summary}\n\nNovo resumo:"
        new_summary = self.llm.predict(prompt)

        # atualiza o resumo acumulado
        self.summary = new_summary.strip()

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
    elif memory_type == "recursive_summarizer":
        memory = RecursiveSummarizerMemory(llm=llm, window_size=5, summarize_every=10)
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
    model = "openai/gpt-oss-20b" # os.environ.get("LANGCHAIN_MODEL")
    memory_type = "recursive_summarizer" # os.environ.get("LANGCHAIN_MEMORY", "buffer")  # default: buffer

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
