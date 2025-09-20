import os
from openai import OpenAI

print(".:: Open AI Playground ::.")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

response = client.responses.create(
    model="gpt-4.1-nano",
    input="Qual a capital do Brasil?"
)

print(response.output_text)

# output
# A capital do Brasil é Brasília.
