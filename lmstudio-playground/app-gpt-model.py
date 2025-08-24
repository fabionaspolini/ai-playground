import lmstudio as lms
# from gpt_oss.tools.python_docker.docker_tool import PythonTool
from openai_harmony import Message, Conversation, Role, load_harmony_encoding, HarmonyEncodingName


print(".:: LM Studio Playground ::.")

SERVER_API_HOST = "localhost:1234"
lms.configure_default_client(SERVER_API_HOST)

model = lms.llm("openai/gpt-oss-20b")
# result = model.respond("Qual a capital do Brasil?")

# Extrai apenas a mensagem final do formato multi-turn chat serialization
# def extrair_mensagem_final(serializado):
#     padrao = r"<\|channel\|>final<\|message\|>(.*?)(?=<\|end\|>|$)"
#     correspondencias = re.findall(padrao, serializado, re.DOTALL)
#     if correspondencias:
#         return correspondencias[-1].strip()
#     return serializado
# 
# if isinstance(result.content, str):
#     print(extrair_mensagem_final(result.content))
# else:
#     print(result.content)
# 

encoding = load_harmony_encoding(HarmonyEncodingName.HARMONY_GPT_OSS)

# create the overall prompt
messages = [Message.from_role_and_content(Role.USER, "Qual a capital do Brasil?")]
conversation = Conversation.from_messages(messages)

# convert to tokens
token_ids = encoding.render_conversation_for_completion(conversation, Role.ASSISTANT)

# perform inference
# ...
response = model.respond("Qual a capital do Brasil?")
output_tokens = model.tokenize(response)
# output_tokens = response.

# parse the output
messages = encoding.parse_messages_from_completion_tokens(output_tokens, Role.ASSISTANT)
print(messages)