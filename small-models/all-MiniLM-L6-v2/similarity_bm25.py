from rank_bm25 import BM25Okapi
import re

# 1. Dados e Tokenização
base_conhecimento = [
    "Instruções para alterar sua credencial de acesso.",
    "O tempo hoje está ensolarado.",
    "Passo a passo para recuperação de conta e login.",
    "Comprar pão na padaria da esquina.",
    "Como resetar minha senha?",
    "Onde encontro a nota fiscal?",
    "Passo a passo para trocar o e-mail.",
    "Política de reembolso e devolução.",
    "Atualização de credenciais"
]

# BM25 trabalha com listas de palavras (tokens)
def tokenize(text):
    return re.sub(r'[^\w\s]', '', text.lower()).split()

tokenized_corpus = [tokenize(doc) for doc in base_conhecimento]

# 2. Inicializar o Algoritmo
bm25 = BM25Okapi(tokenized_corpus)

# 3. Preparar a Consulta
# query = "Esqueci minha credencial de acesso"
# query = "Como posso resetar minha senha?"
query = "perdi meu acesso e login"
tokenized_query = tokenize(query)

# 4. Calcular Scores
# Diferente do Cosseno (0 a 1), o score BM25 não tem limite superior fixo
doc_scores = bm25.get_scores(tokenized_query)

# 5. Obter os N melhores resultados
top_n = bm25.get_top_n(tokenized_query, base_conhecimento, n=len(base_conhecimento))

print(f"Consulta: {query}\n")
for i, doc in enumerate(top_n):
    print(f"Top {i+1}: {doc} (Score: {doc_scores[base_conhecimento.index(doc)]:.4f})")


# query = "Esqueci minha credencial de acesso"
# Top 1: Instruções para alterar sua credencial de acesso. (Score: 3.3185) <----- Útil 1
# Top 2: Como resetar minha senha? (Score: 1.9992) <----- Útil 2
# Top 3: Atualização de credenciais (Score: 0.2546) <----- Útil 3
# Top 4: Política de reembolso e devolução. (Score: 0.2119)
# Top 5: Passo a passo para recuperação de conta e login. (Score: 0.1587) <----- Útil 4
# Top 6: Onde encontro a nota fiscal? (Score: 0.0000)
# Top 7: Passo a passo para trocar o e-mail. (Score: 0.0000)
# Top 8: Comprar pão na padaria da esquina. (Score: 0.0000)
# Top 9: O tempo hoje está ensolarado. (Score: 0.0000)

# query = "Como posso resetar minha senha?"
# Top 1: Como resetar minha senha? (Score: 7.9968) <----- Útil 1
# Top 2: Atualização de credenciais (Score: 0.0000) <----- Útil 2
# Top 3: Política de reembolso e devolução. (Score: 0.0000)
# Top 4: Passo a passo para trocar o e-mail. (Score: 0.0000)
# Top 5: Onde encontro a nota fiscal? (Score: 0.0000)
# Top 6: Comprar pão na padaria da esquina. (Score: 0.0000)
# Top 7: Passo a passo para recuperação de conta e login. (Score: 0.0000) <----- Útil 7
# Top 8: O tempo hoje está ensolarado. (Score: 0.0000)
# Top 9: Instruções para alterar sua credencial de acesso. (Score: 0.0000) <----- Útil 9

# query = "perdi meu acesso e login"
# Top 1: Passo a passo para recuperação de conta e login. (Score: 2.2402) <----- Útil 1
# Top 2: Instruções para alterar sua credencial de acesso. (Score: 1.5685) <----- Útil 2
# Top 3: Política de reembolso e devolução. (Score: 1.1600)
# Top 4: Atualização de credenciais (Score: 0.0000) <----- Útil 4
# Top 5: Passo a passo para trocar o e-mail. (Score: 0.0000)
# Top 6: Como resetar minha senha? (Score: 0.0000) <----- Útil 6
# Top 7: Onde encontro a nota fiscal? (Score: 0.0000)
# Top 8: Comprar pão na padaria da esquina. (Score: 0.0000)
# Top 9: O tempo hoje está ensolarado. (Score: 0.0000)