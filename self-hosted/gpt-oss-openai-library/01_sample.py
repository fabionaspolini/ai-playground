from openai import OpenAI
from openai.types.chat import ChatCompletionSystemMessageParam, ChatCompletionUserMessageParam

print(".:: self-hosted / gpt-oss-openai-library / 01_sample.py ::.")

client = OpenAI(base_url="http://localhost:1234/v1")

response = client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=[
        {"role": "system", "content": "Você é um assistente de uso pessoal em conhecimentos gerais."},
        {"role": "user", "content": "Qual a capital do Brasil?"}
    ],
    # messages=[
    #     ChatCompletionSystemMessageParam(content="Você é um assistente de uso pessoal em conhecimentos gerais.", role="system"),
    #     ChatCompletionUserMessageParam(content="Qual a capital do Brasil?", role="user"),
    # ],
    temperature=0.1
)

# normalmente o conteúdo user-facing já virá em resp.choices[0].message.content
print(response.choices[0].message.content)

# Output
# A capital do Brasil é **Brasília**.