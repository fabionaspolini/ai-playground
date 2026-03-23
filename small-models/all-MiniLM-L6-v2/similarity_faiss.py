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

# 2. Gerar Embeddings (devem ser float32 para o FAISS)
embeddings = model.encode(base_conhecimento).astype('float32')

# 3. Criar o Index FAISS (IndexFlatL2 usa distância Euclidiana)
d = embeddings.shape[1]  # Dimensão do vetor (384 para o MiniLM)
index = faiss.IndexFlatL2(d)
index.add(embeddings)   # Adiciona os vetores ao índice

# 4. Preparar a Consulta
# query = "Esqueci minha credencial de acesso"
# query = "Como posso resetar minha senha?"
query = "perdi meu acesso e login"
query_embedding = model.encode([query]).astype('float32')

# 5. Buscar os K vizinhos mais próximos
k = len(base_conhecimento)  # Top 2 resultados
distancias, indices = index.search(query_embedding, k)

# 6. Resultados
print(f"Consulta: {query}\n")
for i, idx in enumerate(indices[0]):
    print(f"Top {i+1}: {base_conhecimento[idx]} (Distância: {distancias[0][i]:.4f})")

# query = "Esqueci minha credencial de acesso"
# Top 1: Instruções para alterar sua credencial de acesso. (Distância: 0.6275) <----- Útil 1
# Top 2: Comprar pão na padaria da esquina. (Distância: 0.8821)
# Top 3: Como resetar minha senha? (Distância: 0.8919) <----- Útil 3
# Top 4: Atualização de credenciais (Distância: 0.9305) <----- Útil 4
# Top 5: Política de reembolso e devolução. (Distância: 1.0482)
# Top 6: O tempo hoje está ensolarado. (Distância: 1.1688)
# Top 7: Passo a passo para trocar o e-mail. (Distância: 1.1833)
# Top 8: Passo a passo para recuperação de conta e login. (Distância: 1.3278) <----- Útil 8
# Top 9: Onde encontro a nota fiscal? (Distância: 1.4457)

# query = "Como posso resetar minha senha?"
# Top 1: Como resetar minha senha? (Distância: 0.1216) <----- Útil 1
# Top 2: O tempo hoje está ensolarado. (Distância: 0.9632)
# Top 3: Instruções para alterar sua credencial de acesso. (Distância: 1.0245) <----- Útil 3
# Top 4: Passo a passo para trocar o e-mail. (Distância: 1.0595)
# Top 5: Comprar pão na padaria da esquina. (Distância: 1.1204)
# Top 6: Passo a passo para recuperação de conta e login. (Distância: 1.1442) <----- Útil 6
# Top 7: Política de reembolso e devolução. (Distância: 1.2334)
# Top 8: Atualização de credenciais (Distância: 1.2426) <----- Útil 8
# Top 9: Onde encontro a nota fiscal? (Distância: 1.3465)

# query = "perdi meu acesso e login"
# Top 1: Passo a passo para recuperação de conta e login. (Distância: 0.8124) <----- Útil 1
# Top 2: Instruções para alterar sua credencial de acesso. (Distância: 0.9993) <----- Útil 2
# Top 3: Passo a passo para trocar o e-mail. (Distância: 1.0161)
# Top 4: Como resetar minha senha? (Distância: 1.2324) <----- Útil 3
# Top 5: O tempo hoje está ensolarado. (Distância: 1.2403)
# Top 6: Política de reembolso e devolução. (Distância: 1.2490)
# Top 7: Comprar pão na padaria da esquina. (Distância: 1.2943)
# Top 8: Atualização de credenciais (Distância: 1.4360) <----- Útil 8
# Top 9: Onde encontro a nota fiscal? (Distância: 1.4997)