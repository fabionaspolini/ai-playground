# Relatório de Testes de Similaridade

**Dataset:** dataset_credenciais.json

**Queries testadas:** 3


## Resultados Detalhados


Os valores por query, são os **ranks** de onde cada resposta útil foi calculada pelo algoritmo.

| Modelo | Algoritmo | Query 1 | Query 2 | Query 3 | Rank Médio | Tempo Total (s) | Tempo Médio (s) |
|--------|-----------|--------|--------|--------|-----------|-----------------|-----------------|
| N/A (lexical) | BM25 | 1, 2, 3, 5 | 1, 2, 7, 9 | 1, 2, 4, 6 | **3.58** | 0.000 | 0.000 |
| sentence-transformers/all-MiniLM-L6-v2 | Cosine Similarity | 1, 3, 4, 8 | 1, 3, 6, 8 | 1, 2, 4, 8 | **4.08** | 0.024 | 0.008 |
| sentence-transformers/all-MiniLM-L6-v2 | FAISS Cosine | 1, 3, 4, 8 | 1, 3, 6, 8 | 1, 2, 4, 8 | **4.08** | 0.023 | 0.008 |
| sentence-transformers/all-MiniLM-L6-v2 | FAISS Euclidean | 1, 3, 4, 8 | 1, 3, 6, 8 | 1, 2, 4, 8 | **4.08** | 0.025 | 0.008 |
| sentence-transformers/all-MiniLM-L6-v2 | ChromaDB | 1, 3, 4, 8 | 1, 3, 6, 8 | 1, 2, 4, 8 | **4.08** | 0.031 | 0.010 |
| paraphrase-multilingual-MiniLM-L12-v2 | Cosine Similarity | 1, 2, 3, 4 | 1, 2, 3, 5 | 1, 2, 3, 6 | **2.75** | 0.050 | 0.017 |
| paraphrase-multilingual-MiniLM-L12-v2 | FAISS Cosine | 1, 2, 3, 4 | 1, 2, 3, 5 | 1, 2, 3, 6 | **2.75** | 0.047 | 0.016 |
| paraphrase-multilingual-MiniLM-L12-v2 | FAISS Euclidean | 1, 2, 3, 4 | 1, 2, 3, 6 | 1, 2, 3, 6 | **2.83** | 0.052 | 0.017 |
| paraphrase-multilingual-MiniLM-L12-v2 | ChromaDB | 1, 2, 3, 4 | 1, 2, 3, 6 | 1, 2, 3, 6 | **2.83** | 0.064 | 0.021 |
| neuralmind/bert-base-portuguese-cased | Cosine Similarity | 1, 2, 3, 4 | 1, 2, 3, 6 | 1, 2, 3, 5 | **2.75** | 0.117 | 0.039 |
| neuralmind/bert-base-portuguese-cased | FAISS Cosine | 1, 2, 3, 4 | 1, 2, 3, 6 | 1, 2, 3, 5 | **2.75** | 0.125 | 0.042 |
| neuralmind/bert-base-portuguese-cased | FAISS Euclidean | 1, 2, 3, 4 | 1, 2, 3, 5 | 1, 2, 3, 5 | **2.67** | 0.117 | 0.039 |
| neuralmind/bert-base-portuguese-cased | ChromaDB | 1, 2, 3, 4 | 1, 2, 3, 5 | 1, 2, 3, 5 | **2.67** | 0.121 | 0.040 |
| BAAI/bge-m3 | Cosine Similarity | 1, 2, 3, 4 | 1, 2, 3, 4 | 1, 2, 3, 4 | **2.50** | 0.416 | 0.139 |
| BAAI/bge-m3 | FAISS Cosine | 1, 2, 3, 4 | 1, 2, 3, 4 | 1, 2, 3, 4 | **2.50** | 0.401 | 0.134 |
| BAAI/bge-m3 | FAISS Euclidean | 1, 2, 3, 4 | 1, 2, 3, 4 | 1, 2, 3, 4 | **2.50** | 0.364 | 0.121 |
| BAAI/bge-m3 | ChromaDB | 1, 2, 3, 4 | 1, 2, 3, 4 | 1, 2, 3, 4 | **2.50** | 0.406 | 0.135 |

## Consolidado por Modelo


| Modelo | Média Geral |
|--------|-------------|
| N/A (lexical) | **3.58** |
| sentence-transformers/all-MiniLM-L6-v2 | **4.08** |
| paraphrase-multilingual-MiniLM-L12-v2 | **2.79** |
| neuralmind/bert-base-portuguese-cased | **2.71** |
| BAAI/bge-m3 | **2.50** |

## Conclusão


O melhor desempenho foi de **Cosine Similarity** com modelo **BAAI/bge-m3** (rank médio: **2.50**).


## Top 10 Respostas Selecionadas pelo Algoritmo Vencedor


*As respostas em **negrito** são as respostas úteis esperadas.*


### Query 1: Esqueci minha credencial de acesso


| # | Resposta |
|---|----------|
| 1 | **Como resetar minha senha?** |
| 2 | **Instruções para alterar sua credencial de acesso.** |
| 3 | **Atualização de credenciais** |
| 4 | **Passo a passo para recuperação de conta e login.** |
| 5 | Passo a passo para trocar o e-mail. |
| 6 | Política de reembolso e devolução. |
| 7 | Comprar pão na padaria da esquina. |
| 8 | Onde encontro a nota fiscal? |
| 9 | O tempo hoje está ensolarado. |

*Nota: A base de conhecimento possui apenas 9 documento(s).*

### Query 2: Como posso resetar minha senha?


| # | Resposta |
|---|----------|
| 1 | **Como resetar minha senha?** |
| 2 | **Instruções para alterar sua credencial de acesso.** |
| 3 | **Passo a passo para recuperação de conta e login.** |
| 4 | **Atualização de credenciais** |
| 5 | Passo a passo para trocar o e-mail. |
| 6 | Política de reembolso e devolução. |
| 7 | Onde encontro a nota fiscal? |
| 8 | Comprar pão na padaria da esquina. |
| 9 | O tempo hoje está ensolarado. |

*Nota: A base de conhecimento possui apenas 9 documento(s).*

### Query 3: perdi meu acesso e login


| # | Resposta |
|---|----------|
| 1 | **Passo a passo para recuperação de conta e login.** |
| 2 | **Como resetar minha senha?** |
| 3 | **Instruções para alterar sua credencial de acesso.** |
| 4 | **Atualização de credenciais** |
| 5 | Passo a passo para trocar o e-mail. |
| 6 | Política de reembolso e devolução. |
| 7 | Onde encontro a nota fiscal? |
| 8 | Comprar pão na padaria da esquina. |
| 9 | O tempo hoje está ensolarado. |

*Nota: A base de conhecimento possui apenas 9 documento(s).*
