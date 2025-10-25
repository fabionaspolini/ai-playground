from openai import OpenAI

from tools import *

print(".:: agents / clima ::.")

client = OpenAI(base_url="http://localhost:1234/v1")

messages = [{"role": "user", "content": "Qual temperatura no CEP 88804-495?"}]

response = client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=,
    tools=tools,
    temperature=0.1
)

if response.choices[0].message.tool_calls:
    tool_call = response.choices[0].message.tool_calls[0]
    result = execute_tool(tool_call)
    print(f"Resultado da ferramenta '{tool_call.function.name}': {result}")

# print(response.choices[0].message.content)

# tool_call = response.choices[0].message.tool_calls[0]
# teste = execute_tool(tool_call)

# location = eval(tool_call.function.arguments)["location"]
# 
# weather = get_weather(location)
# print(weather)