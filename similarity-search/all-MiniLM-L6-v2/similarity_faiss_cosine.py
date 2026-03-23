import faiss
from sentence_transformers import SentenceTransformer

# 1. Modelo e Dados
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
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

# 2. Gerar Embeddings e Normalizar (Crucial para Cosseno)
embeddings = model.encode(base_conhecimento).astype('float32')
faiss.normalize_L2(embeddings) # Normaliza os vetores na base

# 3. Criar o Index de Produto Interno (IP)
d = embeddings.shape[1]
index = faiss.IndexFlatIP(d)
index.add(embeddings)

# 4. Preparar e Normalizar a Consulta
# query = "Esqueci minha credencial de acesso"
# query = "Como posso resetar minha senha?"
query = "perdi meu acesso e login"
query_embedding = model.encode([query]).astype('float32')
faiss.normalize_L2(query_embedding) # Normaliza o vetor da consulta

# 5. Buscar os K mais similares
k = len(base_conhecimento)
scores, indices = index.search(query_embedding, k)

# 6. Resultados (Scores agora são a Similaridade de Cosseno entre 0 e 1)
print(f"Consulta: {query}\n")
for i, idx in enumerate(indices[0]):
    print(f"Top {i+1}: {base_conhecimento[idx]} (Score: {scores[0][i]:.4f})")

# query = "Esqueci minha credencial de acesso"
# Top 1: Instruções para alterar sua credencial de acesso. (Score: 0.6863) <----- Útil 1
# Top 2: Comprar pão na padaria da esquina. (Score: 0.5589)
# Top 3: Como resetar minha senha? (Score: 0.5540) <----- Útil 3
# Top 4: Atualização de credenciais (Score: 0.5347) <----- Útil 4
# Top 5: Política de reembolso e devolução. (Score: 0.4759)
# Top 6: O tempo hoje está ensolarado. (Score: 0.4156)
# Top 7: Passo a passo para trocar o e-mail. (Score: 0.4084)
# Top 8: Passo a passo para recuperação de conta e login. (Score: 0.3361) <----- Útil 8
# Top 9: Onde encontro a nota fiscal? (Score: 0.2772)

# query = "Como posso resetar minha senha?"
# Top 1: Como resetar minha senha? (Score: 0.9392) <----- Útil 1
# Top 2: O tempo hoje está ensolarado. (Score: 0.5184)
# Top 3: Instruções para alterar sua credencial de acesso. (Score: 0.4877) <----- Útil 3
# Top 4: Passo a passo para trocar o e-mail. (Score: 0.4702)
# Top 5: Comprar pão na padaria da esquina. (Score: 0.4398)
# Top 6: Passo a passo para recuperação de conta e login. (Score: 0.4279) <----- Útil 6
# Top 7: Política de reembolso e devolução. (Score: 0.3833)
# Top 8: Atualização de credenciais (Score: 0.3787) <----- Útil 8
# Top 9: Onde encontro a nota fiscal? (Score: 0.3268)

# query = "perdi meu acesso e login"
# Top 1: Passo a passo para recuperação de conta e login. (Score: 0.5938) <----- Útil 1
# Top 2: Instruções para alterar sua credencial de acesso. (Score: 0.5003) <----- Útil 2
# Top 3: Passo a passo para trocar o e-mail. (Score: 0.4920)
# Top 4: Como resetar minha senha? (Score: 0.3838) <----- Útil 4
# Top 5: O tempo hoje está ensolarado. (Score: 0.3798)
# Top 6: Política de reembolso e devolução. (Score: 0.3755)
# Top 7: Comprar pão na padaria da esquina. (Score: 0.3529)
# Top 8: Atualização de credenciais (Score: 0.2820) <----- Útil 8
# Top 9: Onde encontro a nota fiscal? (Score: 0.2501)