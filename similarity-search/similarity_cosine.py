from sentence_transformers import SentenceTransformer, util

# 1. Carregar o modelo (Small & Efficient)
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# 2. Dados de entrada
# usuario_msg = "Esqueci minha credencial de acesso"
# usuario_msg = "Como posso resetar minha senha?"
usuario_msg = "perdi meu acesso e login"
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

# 3. Gerar os embeddings (vetores numéricos)
embedding_usuario = model.encode(usuario_msg)
embeddings_base = model.encode(base_conhecimento)

# 4. Calcular similaridade de cosseno
scores = util.cos_sim(embedding_usuario, embeddings_base)[0]

# 5. Organizar e exibir resultados
resultados = []
for i, texto in enumerate(base_conhecimento):
    resultados.append({"texto": texto, "score": scores[i].item()})

# Ordenar pelos mais similares
resultados = sorted(resultados, key=lambda x: x['score'], reverse=True)

for i, res in enumerate(resultados):
    print(f"Top {i+1} | Score: {res['score']:.4f} | Texto: {res['texto']}")

# usuario_msg = "Esqueci minha credencial de acesso"
# Top 1 | Score: 0.6863 | Texto: Instruções para alterar sua credencial de acesso. <----- Útil 1
# Top 2 | Score: 0.5589 | Texto: Comprar pão na padaria da esquina.
# Top 3 | Score: 0.5540 | Texto: Como resetar minha senha? <----- Útil 3
# Top 4 | Score: 0.5347 | Texto: Atualização de credenciais  <----- Útil 4
# Top 5 | Score: 0.4759 | Texto: Política de reembolso e devolução.
# Top 6 | Score: 0.4156 | Texto: O tempo hoje está ensolarado.
# Top 7 | Score: 0.4084 | Texto: Passo a passo para trocar o e-mail.
# Top 8 | Score: 0.3361 | Texto: Passo a passo para recuperação de conta e login.  <----- Útil 8
# Top 9 | Score: 0.2772 | Texto: Onde encontro a nota fiscal?

# usuario_msg = "Como posso resetar minha senha?"
# Top 1 | Score: 0.9392 | Texto: Como resetar minha senha? <----- Útil 1
# Top 2 | Score: 0.5184 | Texto: O tempo hoje está ensolarado.
# Top 3 | Score: 0.4877 | Texto: Instruções para alterar sua credencial de acesso. <----- Útil 3
# Top 4 | Score: 0.4702 | Texto: Passo a passo para trocar o e-mail.
# Top 5 | Score: 0.4398 | Texto: Comprar pão na padaria da esquina.
# Top 6 | Score: 0.4279 | Texto: Passo a passo para recuperação de conta e login. <----- Útil 6
# Top 7 | Score: 0.3833 | Texto: Política de reembolso e devolução.
# Top 8 | Score: 0.3787 | Texto: Atualização de credenciais <----- Útil 8
# Top 9 | Score: 0.3268 | Texto: Onde encontro a nota fiscal?

# usuario_msg = "perdi meu acesso e login"
# Top 1 | Score: 0.5938 | Texto: Passo a passo para recuperação de conta e login. <----- Útil 1
# Top 2 | Score: 0.5003 | Texto: Instruções para alterar sua credencial de acesso. <----- Útil 2
# Top 3 | Score: 0.4920 | Texto: Passo a passo para trocar o e-mail.
# Top 4 | Score: 0.3838 | Texto: Como resetar minha senha? <----- Útil 4
# Top 5 | Score: 0.3798 | Texto: O tempo hoje está ensolarado.
# Top 6 | Score: 0.3755 | Texto: Política de reembolso e devolução.
# Top 7 | Score: 0.3529 | Texto: Comprar pão na padaria da esquina.
# Top 8 | Score: 0.2820 | Texto: Atualização de credenciais <----- Útil 8
# Top 9 | Score: 0.2501 | Texto: Onde encontro a nota fiscal?