from openai import OpenAI

print(".:: 4-tools-function-call ::.")

client = OpenAI(base_url="http://localhost:1234/v1")

def get_weather(location):
    return f"{location}: Next Tuesday you will befriend a baby otter."

tools = [
    {
        "type": "function",
        "function":{
            "name": "get_weather",
            "description": "Get current temperature for a given location.",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "City and country e.g. Bogotá, Colombia",
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
    messages=[{"role": "user", "content": "What is the weather like in Paris today?"}],
    tools=tools,
    temperature=0.1
)

# print(response.choices[0].message.content)
tool_call = response.choices[0].message.tool_calls[0]
location = eval(tool_call.function.arguments)["location"]

weather = get_weather(location)
print(weather)