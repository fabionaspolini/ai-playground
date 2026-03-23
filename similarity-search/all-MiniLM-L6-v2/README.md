Comaração de algoritimos de busca por similaridade.

## Buscas Semântica

Busca semântica converte texto em vetores e compara similaridade entre eles. Esse método possui capacidade de identificar intenções.
Desempenho: Rápido.

- similarity_chromadb
- similarity_cosine
- similarity_faiss_cosine
- similarity_faiss_euclidean

## Busca Lexical

Busca lexical funciona baseado na frequência de palavras.
Desempenho: Muito rápido.

- similarity_bm25

---

## Resultados dos Testes - all-MiniLM-L6-v2

Foram realizados 3 testes de consulta com 9 itens na base de conhecimento. Abaixo, o **rank médio** de cada algoritmo considerando apenas os resultados marcados como **úteis**:

| Algoritmo | Tipo | Query 1: "Esqueci minha credencial de acesso" | Query 2: "Como posso resetar minha senha?" | Query 3: "perdi meu acesso e login" | Rank Médio |
|-----------|------|-----------------------------------------------|--------------------------------------------|-------------------------------------|------------|
| **BM25** | Lexical | 1, 2, 3, 5 | 1, 2, 7, 9 | 1, 2, 4, 6 | **3,58** |
| **ChromaDB** | Semântico (Cosseno) | 1, 3, 4, 8 | 1, 3, 6, 8 | 1, 2, 4, 8 | **4,13** |
| **Cosine Similarity** | Semântico (Cosseno) | 1, 3, 4, 8 | 1, 3, 6, 8 | 1, 2, 4, 8 | **4,13** |
| **FAISS Cosine** | Semântico (Cosseno) | 1, 3, 4, 8 | 1, 3, 6, 8 | 1, 2, 4, 8 | **4,13** |
| **FAISS Euclidean** | Semântico (Euclidiana) | 1, 3, 4, 8 | 1, 3, 6, 8 | 1, 2, 4, 8 | **4,13** |

> **Nota:** Os algoritmos baseados em similaridade de cosseno (ChromaDB, Cosine Similarity, FAISS Cosine) produziram resultados idênticos, pois utilizam o mesmo modelo de embeddings (`all-MiniLM-L6-v2`) e a mesma métrica de similaridade. O FAISS Euclidean também apresentou resultados equivalentes, já que a distância euclidiana em vetores normalizados é matematicamente relacionada à similaridade de cosseno.

## Conclusão

O **BM25 (busca lexical)** teve o melhor desempenho geral com rank médio de **3,58**, superando os métodos semânticos em consultas onde as palavras-chave da query estavam bem representadas nos documentos.

**Observações importantes:**

1. **BM25** se destacou por capturar exatamente os termos das consultas, sendo ideal quando há sobreposição lexical entre query e documentos.

2. **Métodos semânticos** (todos com rank médio de 4,13) têm a vantagem de identificar intenções e sinônimos, mesmo sem sobreposição exata de palavras — o que pode ser mais robusto em cenários do mundo real.

3. A escolha do algoritmo deve considerar o caso de uso:
   - Use **BM25** para buscas diretas com termos específicos.
   - Use **métodos semânticos** para entender contexto, intenções e variações linguísticas.

## Modelos

### all-MiniLM-L6-v2
Modelo treinado em inglês, por isso o mal resultado em português.

### paraphrase-multilingual-MiniLM-L12-v2

Multilíngue (Evolução) - Dobro de camadas do L6, muito mais preciso em PT-BR.

### Principais Modelos para Português (PT-BR)
- **BERTimbau (NeuralMind)** → `neuralmind/bert-base-portuguese-cased`: É o padrão ouro para PT-BR. Existe nas versões base e large. Para Sentence-Transformers, utilizamos versões dele ajustadas para similaridade (STS).
- **Sentence-BERT-PT**: Modelos baseados no BERTimbau afinados em datasets como o ASSIN2 (o principal benchmark de similaridade semântica em português).
- **BGE-Small-pt (ou variantes)* → `BAAI/bge-m3`*: Embora o BGE seja multilíngue, versões destiladas com foco em português têm surgido no Hugging Face com excelente performance em RAG. Modelo atual mais forte para múltiplos idiomas, incluindo PT-BR.
