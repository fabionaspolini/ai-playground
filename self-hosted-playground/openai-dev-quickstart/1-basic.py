from openai import OpenAI

print(".:: 1-basic ::.")

client = OpenAI(base_url="http://localhost:1234/v1")

response = client.responses.create(
    model="openai/gpt-oss-20b",
    input="Qual a capital do Brasil?",
    temperature=0.1)

print(response.output_text)
