# Relatório de Testes de Similaridade

**Dataset:** dataset_credenciais.json

**Queries testadas:** 3


## Resultados Detalhados


Os valores por query, são os **ranks** de onde cada resposta útil foi calculada pelo algoritmo.

| Modelo | Algoritmo | Query 1 | Query 2 | Query 3 | Rank Médio | Tempo (s) | CPU (%) | Memória (MB) |
|--------|-----------|--------|--------|--------|-----------|-----------|---------|--------------|
| N/A (lexical) | BM25 | 1, 2, 3, 5 | 1, 2, 7, 9 | 1, 2, 4, 6 | **3.58** | 0.001 | 0.0 | 0.04 |
| sentence-transformers/all-MiniLM-L6-v2 | Cosine Similarity | 1, 3, 4, 8 | 1, 3, 6, 8 | 1, 2, 4, 8 | **4.08** | 0.040 | 0.0 | 0.05 |
| sentence-transformers/all-MiniLM-L6-v2 | FAISS Cosine | 1, 3, 4, 8 | 1, 3, 6, 8 | 1, 2, 4, 8 | **4.08** | 0.045 | 0.0 | 0.05 |
| sentence-transformers/all-MiniLM-L6-v2 | FAISS Euclidean | 1, 3, 4, 8 | 1, 3, 6, 8 | 1, 2, 4, 8 | **4.08** | 0.037 | 0.0 | 0.05 |
| sentence-transformers/all-MiniLM-L6-v2 | ChromaDB | 1, 3, 4, 8 | 1, 3, 6, 8 | 1, 2, 4, 8 | **4.08** | 0.051 | 0.0 | 0.07 |
| paraphrase-multilingual-MiniLM-L12-v2 | Cosine Similarity | 1, 2, 3, 4 | 1, 2, 3, 5 | 1, 2, 3, 6 | **2.75** | 0.058 | 0.0 | 0.05 |
| paraphrase-multilingual-MiniLM-L12-v2 | FAISS Cosine | 1, 2, 3, 4 | 1, 2, 3, 5 | 1, 2, 3, 6 | **2.75** | 0.058 | 0.0 | 0.05 |
| paraphrase-multilingual-MiniLM-L12-v2 | FAISS Euclidean | 1, 2, 3, 4 | 1, 2, 3, 6 | 1, 2, 3, 6 | **2.83** | 0.057 | 0.0 | 0.05 |
| paraphrase-multilingual-MiniLM-L12-v2 | ChromaDB | 1, 2, 3, 4 | 1, 2, 3, 6 | 1, 2, 3, 6 | **2.83** | 0.074 | 0.0 | 0.06 |
| neuralmind/bert-base-portuguese-cased | Cosine Similarity | 1, 2, 3, 4 | 1, 2, 3, 6 | 1, 2, 3, 5 | **2.75** | 0.121 | 0.0 | 0.05 |
| neuralmind/bert-base-portuguese-cased | FAISS Cosine | 1, 2, 3, 4 | 1, 2, 3, 6 | 1, 2, 3, 5 | **2.75** | 0.123 | 0.0 | 0.05 |
| neuralmind/bert-base-portuguese-cased | FAISS Euclidean | 1, 2, 3, 4 | 1, 2, 3, 5 | 1, 2, 3, 5 | **2.67** | 0.120 | 0.0 | 0.05 |
| neuralmind/bert-base-portuguese-cased | ChromaDB | 1, 2, 3, 4 | 1, 2, 3, 5 | 1, 2, 3, 5 | **2.67** | 0.154 | 0.0 | 0.07 |

## Consolidado por Modelo


| Modelo | Média Geral |
|--------|-------------|
| N/A (lexical) | **3.58** |
| sentence-transformers/all-MiniLM-L6-v2 | **4.08** |
| paraphrase-multilingual-MiniLM-L12-v2 | **2.79** |
| neuralmind/bert-base-portuguese-cased | **2.71** |

## Conclusão


O melhor desempenho foi de **FAISS Euclidean** com modelo **neuralmind/bert-base-portuguese-cased** (rank médio: **2.67**).


## Top 10 Respostas Selecionadas pelo Algoritmo Vencedor


*As respostas em **negrito** são as respostas úteis esperadas.*


### Query 1: Esqueci minha credencial de acesso


| # | Resposta |
|---|----------|
| 1 | **Instruções para alterar sua credencial de acesso.** |
| 2 | **Como resetar minha senha?** |
| 3 | **Passo a passo para recuperação de conta e login.** |
| 4 | **Atualização de credenciais** |
| 5 | Onde encontro a nota fiscal? |
| 6 | Passo a passo para trocar o e-mail. |
| 7 | Política de reembolso e devolução. |
| 8 | Comprar pão na padaria da esquina. |
| 9 | O tempo hoje está ensolarado. |

*Nota: A base de conhecimento possui apenas 9 documento(s).*

### Query 2: Como posso resetar minha senha?


| # | Resposta |
|---|----------|
| 1 | **Como resetar minha senha?** |
| 2 | **Passo a passo para recuperação de conta e login.** |
| 3 | **Instruções para alterar sua credencial de acesso.** |
| 4 | Onde encontro a nota fiscal? |
| 5 | **Atualização de credenciais** |
| 6 | Passo a passo para trocar o e-mail. |
| 7 | Política de reembolso e devolução. |
| 8 | Comprar pão na padaria da esquina. |
| 9 | O tempo hoje está ensolarado. |

*Nota: A base de conhecimento possui apenas 9 documento(s).*

### Query 3: perdi meu acesso e login


| # | Resposta |
|---|----------|
| 1 | **Como resetar minha senha?** |
| 2 | **Passo a passo para recuperação de conta e login.** |
| 3 | **Instruções para alterar sua credencial de acesso.** |
| 4 | Passo a passo para trocar o e-mail. |
| 5 | **Atualização de credenciais** |
| 6 | Onde encontro a nota fiscal? |
| 7 | Política de reembolso e devolução. |
| 8 | Comprar pão na padaria da esquina. |
| 9 | O tempo hoje está ensolarado. |

*Nota: A base de conhecimento possui apenas 9 documento(s).*
