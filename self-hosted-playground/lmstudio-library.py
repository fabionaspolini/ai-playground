import lmstudio as lms
import re
from typing import Dict, List

def simple_harmony_parse(raw: str) -> Dict[str, List[str]]:
    """
    Parse muito simples do formato:
    <|channel|>analysis<|message|>...<|end|><|start|>assistant<|channel|>final<|message|>...
    Retorna dict: {"analysis": [...], "final": [...], ...}
    """
    pattern = re.compile(
        r"<\|channel\|>(?P<chan>\w+)<\|message\|>(?P<msg>.*?)(?=(?:<\|channel\|>\w+<\|message\|>)|$)",
        re.DOTALL,
    )
    segments = {}
    for m in pattern.finditer(raw):
        chan = m.group("chan")
        msg = m.group("msg").strip()
        segments.setdefault(chan, []).append(msg)
    return segments

print(".:: LM Studio Playground ::.")

SERVER_API_HOST = "localhost:1234"
lms.configure_default_client(SERVER_API_HOST)

model = lms.llm("openai/gpt-oss-20b")
response = model.respond("Qual a capital do Brasil?")
response_message = simple_harmony_parse(response.content)

# raw respose:
# {'<|channel|>analysis<|message|>Answer in Portuguese: Brasília.<|end|>
# <|start|>assistant<|channel|>final<|message|>A capital do Brasil é **Brasília**.'}

print("raw response: ", {response.content})
print("response message:", response_message["final"][0])
