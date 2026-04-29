import os
from openai import OpenAI
from openai.types.chat import ChatCompletionUserMessageParam

print(".:: Open AI Playground ::.")

# OpenAI
# LLM_PROVIDER_API_KEY = os.getenv("OPENAI_API_KEY")

# AWS Bedrock
LLM_PROVIDER_BASE_URL = os.getenv("AWS_BEDROCK_BASE_URL")
LLM_PROVIDER_API_KEY = os.getenv("AWS_BEARER_TOKEN_BEDROCK")
# LLM_PROVIDER_BASE_URL = "https://bedrock-runtime.us-east-1.api.aws/v1"

# Lite LLM (localhost)
# LLM_PROVIDER_BASE_URL = "http://0.0.0.0:4000"

# Microsoft Foundry
# LLM_PROVIDER_BASE_URL = os.getenv("AZURE_FOUNDRY_BASE_URL")
# LLM_PROVIDER_API_KEY = os.getenv("AZURE_FOUNDRY_API_KEY")
# MODEL = "Kimi-K2.5" # deployment name

client = OpenAI(api_key=LLM_PROVIDER_API_KEY, base_url=LLM_PROVIDER_BASE_URL)

MODEL = "openai.gpt-oss-20b"
# MODEL = "openai.gpt-oss-120b"
# MODEL = "qwen.qwen3-coder-30b-a3b-v1:0"
# MODEL = "qwen.qwen3-coder-next"
# MODEL = "amazon.nova-micro-v1:0"
# MODEL = "amazon.nova-2-lite-v1:0"
# MODEL = "arn:aws:bedrock:us-east-1:452970698287:inference-profile/us.amazon.nova-2-lite-v1:0" # para bedrock-runtime
# MODEL = "global.amazon.nova-2-lite-v1:0"
# MODEL = "nova-2"
# MODEL = "anthropic.claude-sonnet-4-6"
# MODEL = "us.anthropic.claude-sonnet-4-5-20250929-v1:0" # nao funciona

# Esse exemplo, utiliza nova /v1/responses (introduzido para modelos mais recentes com capacidades de raciocínio, como a série o1/o3)
# response = client.responses.create(
#     model=MODEL,
#     input="Qual a capital do Brasil?"
# )
# print(response.output_text)

response = client.chat.completions.create(
    model=MODEL,
    messages=[ChatCompletionUserMessageParam(role="user", content="Qual a capital do Brasil?")]
    # Evite parâmetros como 'response_format' se o erro persistir
)
print(response.choices[0].message.content)

print()
print("Usage tokens")
print("------------")
print(f"prompt_tokens: {response.usage.prompt_tokens}")
print(f"completion_tokens: {response.usage.completion_tokens}")
print(f"total_tokens: {response.usage.total_tokens}")

# output
# A capital do Brasil é Brasília.
