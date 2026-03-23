# Relatório de Testes de Similaridade

**Dataset:** dataset_credenciais.json

**Queries testadas:** 3


## Resultados Detalhados


| Modelo | Algoritmo | Query 1 | Query 2 | Query 3 | Rank Médio | Tempo (s) | CPU (%) | Memória (MB) |
|--------|-----------|--------|--------|--------|-----------|-----------|---------|--------------|
| N/A (lexical) | BM25 | 1, 2, 3, 5 | 1, 2, 7, 9 | 1, 2, 4, 6 | **3.58** | 0.001 | 0.0 | 0.04 |
| sentence-transformers/all-MiniLM-L6-v2 | Cosine Similarity | 1, 3, 4, 8 | 1, 3, 6, 8 | 1, 2, 4, 8 | **4.08** | 0.051 | 0.0 | 0.05 |
| sentence-transformers/all-MiniLM-L6-v2 | FAISS Cosine | 1, 3, 4, 8 | 1, 3, 6, 8 | 1, 2, 4, 8 | **4.08** | 0.048 | 0.0 | 0.05 |
| sentence-transformers/all-MiniLM-L6-v2 | FAISS Euclidean | 1, 3, 4, 8 | 1, 3, 6, 8 | 1, 2, 4, 8 | **4.08** | 0.038 | 0.0 | 0.05 |
| sentence-transformers/all-MiniLM-L6-v2 | ChromaDB | 1, 3, 4, 8 | 1, 3, 6, 8 | 1, 2, 4, 8 | **4.08** | 0.044 | 0.0 | 0.06 |
| BAAI/bge-m3 | Cosine Similarity | 1, 2, 3, 4 | 1, 2, 3, 4 | 1, 2, 3, 4 | **2.50** | 0.523 | 0.0 | 0.05 |
| BAAI/bge-m3 | FAISS Cosine | 1, 2, 3, 4 | 1, 2, 3, 4 | 1, 2, 3, 4 | **2.50** | 0.468 | 0.0 | 0.05 |
| BAAI/bge-m3 | FAISS Euclidean | 1, 2, 3, 4 | 1, 2, 3, 4 | 1, 2, 3, 4 | **2.50** | 0.689 | 0.0 | 0.05 |
| BAAI/bge-m3 | ChromaDB | 1, 2, 3, 4 | 1, 2, 3, 4 | 1, 2, 3, 4 | **2.50** | 0.621 | 0.0 | 0.08 |

## Consolidado por Modelo


| Modelo | Média Geral |
|--------|-------------|
| N/A (lexical) | **3.58** |
| sentence-transformers/all-MiniLM-L6-v2 | **4.08** |
| BAAI/bge-m3 | **2.50** |

## Conclusão


O melhor desempenho foi de **Cosine Similarity** com modelo **BAAI/bge-m3** (rank médio: **2.50**).

