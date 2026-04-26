import time
from openai import OpenAI

client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

def benchmark():
    start_time = time.time()

    prompt = "Gerar 25 palavas aleatórias. Retorne apenas as palavras separadas por vírgula"
    # prompt = "Escreva um texto longo sobre computação quântica."

    response = client.chat.completions.create(
        model="qwen3.5:9b",
        messages=[{"role": "user", "content": prompt}],
        stream=False
    )

    end_time = time.time()
    duration = end_time - start_time
    
    print(response.choices[0].message.content)
    print("-" * 80)

    # O objeto 'usage' contém os números exatos para o cálculo
    tokens_gerados = response.usage.completion_tokens
    tps = tokens_gerados / duration

    print(f"Tokens Gerados: {tokens_gerados}")
    print(f"Tempo Total: {duration:.2f}s")
    print(f"Tokens por Segundo: {tps:.2f} TPS")

benchmark()