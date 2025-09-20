import lmstudio as lms

print(".:: LM Studio Playground ::.")

SERVER_API_HOST = "localhost:1234"
lms.configure_default_client(SERVER_API_HOST)

model = lms.llm("openai/gpt-oss-20b")
result = model.respond("Qual a capital do Brasil?")

print(result.content)

# Output:
# <|channel|>analysis<|message|>Answer in Portuguese: Brasília.<|end|><|start|>assistant<|channel|>final<|message|>A capital do Brasil é **Brasília**.

# Output by block:
# <|channel|>analysis
# <|message|>Answer in Portuguese: Brasília.
# <|end|>
# <|start|>assistant
# <|channel|>final
# <|message|>A capital do Brasil é **Brasília**.
