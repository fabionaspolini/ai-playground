import os

from openai import OpenAI

print(".:: 2 Analyze Images ::.")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

# fail
response = client.responses.create(
    model="gpt-4.1-nano",
    input=[
        {
            "role": "user",
            "content": [
                {
                    "type": "input_text",
                    "text": "O que está acontecendo nessa imagem?",
                },
                {
                    "type": "input_image",
                    "image_url": "https://images.unsplash.com/photo-1749498982210-3e2de0889fb0?q=80&w=685&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
                }
            ]
        }
    ]
)

print(response.output_text)
