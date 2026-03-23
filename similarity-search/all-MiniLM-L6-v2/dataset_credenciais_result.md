# Relatório de Testes de Similaridade

**Dataset:** dataset_credenciais.json

**Queries testadas:** 3


## Resultados


| Algoritmo | Modelo | Query 1 | Query 2 | Query 3 | Rank Médio | Tempo (s) | CPU (%) | Memória (MB) |
|-----------|--------|--------|--------|--------|-----------|-----------|---------|--------------|
| BM25 | N/A (lexical) | 1, 5, 2, 3 | 9, 7, 1, 2 | 2, 1, 6, 4 | **3.58** | 0.001 | 0.0 | 0.04 |
| Cosine Similarity | sentence-transformers/all-MiniLM-L6-v2 | 1, 8, 3, 4 | 3, 6, 1, 8 | 2, 1, 4, 8 | **4.08** | 3.719 | 0.0 | 10.74 |
| FAISS Cosine | sentence-transformers/all-MiniLM-L6-v2 | 1, 8, 3, 4 | 3, 6, 1, 8 | 2, 1, 4, 8 | **4.08** | 0.070 | 0.0 | 0.05 |
| FAISS Euclidean | sentence-transformers/all-MiniLM-L6-v2 | 1, 8, 3, 4 | 3, 6, 1, 8 | 2, 1, 4, 8 | **4.08** | 0.062 | 0.0 | 0.05 |
| ChromaDB | sentence-transformers/all-MiniLM-L6-v2 | 1, 8, 3, 4 | 3, 6, 1, 8 | 2, 1, 4, 8 | **4.08** | 0.276 | 0.0 | 0.32 |
| Cosine Similarity | paraphrase-multilingual-MiniLM-L12-v2 | 2, 3, 1, 4 | 3, 2, 1, 5 | 3, 1, 2, 6 | **2.75** | 5.759 | 0.0 | 76.31 |
| FAISS Cosine | paraphrase-multilingual-MiniLM-L12-v2 | 2, 3, 1, 4 | 3, 2, 1, 5 | 3, 1, 2, 6 | **2.75** | 0.112 | 0.0 | 0.05 |
| FAISS Euclidean | paraphrase-multilingual-MiniLM-L12-v2 | 1, 2, 3, 4 | 3, 2, 1, 6 | 3, 1, 2, 6 | **2.83** | 0.108 | 0.0 | 0.05 |
| ChromaDB | paraphrase-multilingual-MiniLM-L12-v2 | 1, 2, 3, 4 | 3, 2, 1, 6 | 3, 1, 2, 6 | **2.83** | 0.118 | 0.0 | 0.15 |
| Cosine Similarity | neuralmind/bert-base-portuguese-cased | 2, 3, 1, 4 | 3, 2, 1, 6 | 3, 2, 1, 5 | **2.75** | 2.769 | 0.0 | 1.86 |
| FAISS Cosine | neuralmind/bert-base-portuguese-cased | 2, 3, 1, 4 | 3, 2, 1, 6 | 3, 2, 1, 5 | **2.75** | 0.272 | 0.0 | 0.06 |
| FAISS Euclidean | neuralmind/bert-base-portuguese-cased | 1, 3, 2, 4 | 3, 2, 1, 5 | 3, 2, 1, 5 | **2.67** | 0.274 | 0.0 | 0.06 |
| ChromaDB | neuralmind/bert-base-portuguese-cased | 1, 3, 2, 4 | 3, 2, 1, 5 | 3, 2, 1, 5 | **2.67** | 0.303 | 0.0 | 0.28 |
| Cosine Similarity | BAAI/bge-m3 | 2, 4, 1, 3 | 2, 3, 1, 4 | 3, 1, 2, 4 | **2.50** | 7.742 | 0.0 | 184.55 |
| FAISS Cosine | BAAI/bge-m3 | 2, 4, 1, 3 | 2, 3, 1, 4 | 3, 1, 2, 4 | **2.50** | 0.953 | 0.0 | 0.07 |
| FAISS Euclidean | BAAI/bge-m3 | 2, 4, 1, 3 | 2, 3, 1, 4 | 3, 1, 2, 4 | **2.50** | 0.973 | 0.0 | 0.07 |
| ChromaDB | BAAI/bge-m3 | 2, 4, 1, 3 | 2, 3, 1, 4 | 3, 1, 2, 4 | **2.50** | 0.922 | 0.0 | 0.36 |

## Conclusão


O melhor desempenho foi de **Cosine Similarity** com modelo **BAAI/bge-m3** (rank médio: **2.50**).

