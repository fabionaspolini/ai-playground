# usando a biblioteca 'openai' moderna (ex.: OpenAI Python SDK)
from openai import OpenAI

client = OpenAI(base_url="http://localhost:1234/v1")

resp = client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=[
        {"role": "system", "content": "Você é um assistente de uso pessoal em conhecimentos gerais."},
        {"role": "user", "content": "Qual a capital do Brasil?"}
    ],
    temperature=0.1
)

# normalmente o conteúdo user-facing já virá em resp.choices[0].message.content
print(resp.choices[0].message.content)
