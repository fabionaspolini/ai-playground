import lmstudio as lms

model = lms.llm("openai/gpt-oss-20b")
chat = lms.Chat("Você é um assistente de IA focado em tarefas")

while True:
    try:
        user_input = input("Você (leave blank to exit): ")
    except EOFError:
        print()
        break
    if not user_input:
        break
    chat.add_user_message(user_input)
    prediction_stream = model.respond_stream(
        chat,
        on_message=chat.append,
    )
    print("Bot: ", end="", flush=True)
    for fragment in prediction_stream:
        print(fragment.content, end="", flush=True)
    print()

