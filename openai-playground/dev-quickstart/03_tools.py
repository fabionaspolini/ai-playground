import os

from openai import OpenAI

print(".:: 3-tools ::.")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

response = client.responses.create(
    model="gpt-4.1-nano",
    tools=[{"type": "web_search"}],
    input="Quais filmes da Marvel foram, ou serão lançados no ano atual?",
    temperature=0
)

# Exemplo oficial:
# input="What was a positive news story from today?"

# input="Qual placar dos jogos de futebol da semana no campeonato brasileiro?"
# R: Exibe sites para consultar a informação

# input="Extrair do google, o placar dos jogos de futebol da semana no campeonato brasileiro."
# Resposta: Google não oferece API pública, e ele recomendou um script para web scraping ao não informar a temperatura.
# Muito demorado, usa bastante gpu.

# input="Quais filmes da Marvel foram, ou serão lançados no ano atual?",
# Reposta: Alucinada, ele inventou filmes que não existem.

print(response.output_text)