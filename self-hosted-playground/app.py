import lmstudio as lms

print(".:: LM Studio Playground ::.")

SERVER_API_HOST = "localhost:1234"
lms.configure_default_client(SERVER_API_HOST)

model = lms.llm("openai/gpt-oss-20b")
result = model.respond("Qual a capital do Brasil?")

print(result.content)
