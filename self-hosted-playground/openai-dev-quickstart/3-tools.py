from openai import OpenAI

print(".:: 3-tools ::.")

client = OpenAI(base_url="http://localhost:1234/v1")

response = client.responses.create(
    model="openai/gpt-oss-20b",
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