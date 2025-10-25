import json

from openai.types.chat import ChatCompletionMessageCustomToolCall, ChatCompletionMessageFunctionToolCall

# Obrigatório importar todas as ferramentas para que possam ser acessadas via globals()
from agents.clima.tools import *


def execute_tool(tool: ChatCompletionMessageFunctionToolCall | ChatCompletionMessageCustomToolCall) -> str:
    function_name = tool.function.name
    args = json.loads(tool.function.arguments)
    return globals()[function_name](**args)
