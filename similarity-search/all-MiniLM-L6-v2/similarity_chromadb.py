import chromadb
from sentence_transformers import SentenceTransformer

# 1. Configurar Cliente e Modelo
client = chromadb.Client() # Para persistir use: chromadb.PersistentClient(path="./db")
model = SentenceTransformer('all-MiniLM-L6-v2')

# 2. Criar uma Coleção
collection = client.create_collection(name="suporte_cliente")

# 3. Dados de Exemplo
documentos = [
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
ids = ["id1", "id2", "id3", "id4", "id5", "id6", "id7", "id8", "id9"]

# 4. Gerar Embeddings e Adicionar (Chroma armazena IDs e Textos juntos)
embeddings = model.encode(documentos).tolist() # Converte para lista (formato do Chroma)

collection.add(
    embeddings=embeddings,
    documents=documentos,
    ids=ids
)

# 5. Realizar a Busca
# query_text = "Esqueci minha credencial de acesso"
# query_text = "Como posso resetar minha senha?"
query_text = "perdi meu acesso e login"
query_embedding = model.encode([query_text]).tolist()

results = collection.query(
    query_embeddings=query_embedding,
    n_results=len(documentos)
)

# 6. Exibir Resultados
for i in range(len(results['ids'][0])):
    print(f"Top {i+1} | ID: {results['ids'][0][i]} | Texto: {results['documents'][0][i]} | Distância: {results['distances'][0][i]:.4f}")

# query_text = "Esqueci minha credencial de acesso"
# Top 1 | ID: id1 | Texto: Instruções para alterar sua credencial de acesso. | Distância: 0.6275 <----- Útil 1
# Top 2 | ID: id4 | Texto: Comprar pão na padaria da esquina. | Distância: 0.8821
# Top 3 | ID: id5 | Texto: Como resetar minha senha? | Distância: 0.8919 <----- Útil 3
# Top 4 | ID: id9 | Texto: Atualização de credenciais | Distância: 0.9305 <----- Útil 4
# Top 5 | ID: id8 | Texto: Política de reembolso e devolução. | Distância: 1.0482
# Top 6 | ID: id2 | Texto: O tempo hoje está ensolarado. | Distância: 1.1688
# Top 7 | ID: id7 | Texto: Passo a passo para trocar o e-mail. | Distância: 1.1833
# Top 8 | ID: id3 | Texto: Passo a passo para recuperação de conta e login. | Distância: 1.3278  <----- Útil 8
# Top 9 | ID: id6 | Texto: Onde encontro a nota fiscal? | Distância: 1.4457

# query_text = "Como posso resetar minha senha?"
# Top 1 | ID: id5 | Texto: Como resetar minha senha? | Distância: 0.1216 <----- Útil 1
# Top 2 | ID: id2 | Texto: O tempo hoje está ensolarado. | Distância: 0.9632
# Top 3 | ID: id1 | Texto: Instruções para alterar sua credencial de acesso. | Distância: 1.0245 <----- Útil 3
# Top 4 | ID: id7 | Texto: Passo a passo para trocar o e-mail. | Distância: 1.0595
# Top 5 | ID: id4 | Texto: Comprar pão na padaria da esquina. | Distância: 1.1204
# Top 6 | ID: id3 | Texto: Passo a passo para recuperação de conta e login. | Distância: 1.1442 <----- Útil 6
# Top 7 | ID: id8 | Texto: Política de reembolso e devolução. | Distância: 1.2334
# Top 8 | ID: id9 | Texto: Atualização de credenciais | Distância: 1.2426 <----- Útil 8
# Top 9 | ID: id6 | Texto: Onde encontro a nota fiscal? | Distância: 1.3465

# query_text = "perdi meu acesso e login"
# Top 1 | ID: id3 | Texto: Passo a passo para recuperação de conta e login. | Distância: 0.8124 <----- Útil 1
# Top 2 | ID: id1 | Texto: Instruções para alterar sua credencial de acesso. | Distância: 0.9993 <----- Útil 2
# Top 3 | ID: id7 | Texto: Passo a passo para trocar o e-mail. | Distância: 1.0161
# Top 4 | ID: id5 | Texto: Como resetar minha senha? | Distância: 1.2324 <----- Útil 4
# Top 5 | ID: id2 | Texto: O tempo hoje está ensolarado. | Distância: 1.2403
# Top 6 | ID: id8 | Texto: Política de reembolso e devolução. | Distância: 1.2490
# Top 7 | ID: id4 | Texto: Comprar pão na padaria da esquina. | Distância: 1.2943
# Top 8 | ID: id9 | Texto: Atualização de credenciais | Distância: 1.4360 <----- Útil 8
# Top 9 | ID: id6 | Texto: Onde encontro a nota fiscal? | Distância: 1.4997