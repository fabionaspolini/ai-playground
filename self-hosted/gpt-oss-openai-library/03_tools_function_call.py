import os

from openai import OpenAI

print(".:: self-hosted / gpt-oss-openai-library / 03_tools_function_call.py ::.")

client = OpenAI(base_url="http://localhost:1234/v1")

def get_weather(location):
    return f"{location}: Temperatura atual é 30º (Fake function call)."

tools = [
    {
        "type": "function",
        "function":{
            "name": "get_weather",
            "description": "Obter temperatura atual em uma localização.",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "Cidade ou país, exemplo: Bogotá, Colombia",
                    }
                },
                "required": ["location"],
                "additionalProperties": False,
            },
        },
        "strict": True,
    },
]

response = client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=[{"role": "user", "content": "Qual temporatura em Criciúma hoje?"}],
    tools=tools,
    temperature=0.1
)

# print(response.choices[0].message.content)
tool_call = response.choices[0].message.tool_calls[0]
location = eval(tool_call.function.arguments)["location"]

weather = get_weather(location)
print(weather)