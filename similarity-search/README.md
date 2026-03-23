Comaração de algoritimos de busca por similaridade.

## Buscas Semântica

Busca semântica converte texto em vetores e compara similaridade entre eles. 
Esse método possui capacidade de identificar contexto entre as sentenças. Funciona até com sinônimos das palavras.

Desempenho: Rápido.

- similarity_chromadb
- similarity_cosine
- similarity_faiss_cosine
- similarity_faiss_euclidean

## Busca Lexical

Busca lexical funciona baseado apenas na frequência de palavras, e não possui capacidade de entender contextos.
Não possui capacidade de entender sinônimos.

Desempenho: Muito rápido.

- similarity_bm25

---

## Modelos

### all-MiniLM-L6-v2

Modelo treinado em inglês, por isso o mal resultado em português.

### paraphrase-multilingual-MiniLM-L12-v2

Multilíngue (Evolução) - Dobro de camadas do L6, muito mais preciso em PT-BR.

### Principais Modelos para Português (PT-BR)
- **BERTimbau (NeuralMind)** → `neuralmind/bert-base-portuguese-cased`: É o padrão ouro para PT-BR. Existe nas versões base e large. Para Sentence-Transformers, utilizamos versões dele ajustadas para similaridade (STS).
- **Sentence-BERT-PT**: Modelos baseados no BERTimbau afinados em datasets como o ASSIN2 (o principal benchmark de similaridade semântica em português).
- **BGE-Small-pt (ou variantes)* → `BAAI/bge-m3`*: Embora o BGE seja multilíngue, versões destiladas com foco em português têm surgido no Hugging Face com excelente performance em RAG. Modelo atual mais forte para múltiplos idiomas, incluindo PT-BR.

---

## Testes

O arquivo [similarity_tests.py](similarity_tests.py) faz baterias de testes em cima de datasets de dados, e gera um relatório final com as estatísticas.

- [dataset_credenciais.json](dataset_credenciais.json) → [dataset_credenciais_result.md](dataset_credenciais_result.md): Arquivo pequeno criado por humano afim de validar a acurácia dos algoritmos.
- [dataset_investimentos.json](dataset_investimentos.json) → [dataset_investimentos_result.md](dataset_investimentos_result.md): Arquivo grande para testes de performance, totalmente gerado por AI.
  As respostas úteis foram revisadas por humano apenas em carater de enteder se faz sentido, porém não foi revisado totalmente o dataset da base de conhecimento para saber se são realmente as mais relevante para considerar.

### Veredito

Em ambos testes, o algoritmo vencedor foi **Cosine Similarity** com modelo **BAAI/bge-m3** (análise semântica).

Porém, a alta acurácia dele tem custo em processamento e tempo de reposta.

---

## Estrutura do Dataset

Os arquivos de dataset (`dataset_*.json`) seguem a seguinte estrutura:

```json
{
  "base_conhecimento": ["texto 1", "texto 2", "..."],
  "queries": ["pergunta 1", "pergunta 2", "..."],
  "respostas_uteis": [[índices], [índices], "..."]
}
```

### Propriedades

| Propriedade | Tipo | Descrição |
|-------------|------|-----------|
| `base_conhecimento` | `string[]` | Lista de documentos/textos que compõem a base de conhecimento. Cada documento é identificado pelo seu índice (posição) no array. |
| `queries` | `string[]` | Lista de perguntas ou consultas que serão testadas contra a base de conhecimento. |
| `respostas_uteis` | `int[][]` | Matriz de índices referenciais. Cada array interno corresponde a uma query e contém os índices das respostas consideradas relevantes na `base_conhecimento`, ordenadas por relevância (do mais relevante para o menos relevante). |

### Exemplo

```json
{
  "base_conhecimento": [
    "Instruções para alterar sua credencial de acesso.",
    "O tempo hoje está ensolarado.",
    "Passo a passo para recuperação de conta e login."
  ],
  "queries": [
    "Esqueci minha credencial de acesso"
  ],
  "respostas_uteis": [
    [0, 2]
  ]
}
```

No exemplo acima:
- A query `"Esqueci minha credencial de acesso"` tem como respostas relevantes:
  - Índice `0`: *"Instruções para alterar sua credencial de acesso."* (mais relevante)
  - Índice `2`: *"Passo a passo para recuperação de conta e login."* (segunda mais relevante)

### Critérios para Construção do Dataset

1. **base_conhecimento**: Deve conter textos completos e autocontidos, preferencialmente com 1-3 frases cada.
2. **queries**: Devem simular perguntas reais de usuários, com linguagem natural.
3. **respostas_uteis**: 
   - Os índices devem referenciar posições válidas em `base_conhecimento`
   - A ordem importa: o primeiro índice é a resposta mais relevante
   - Recomenda-se entre 3-10 respostas úteis por query para testes equilibrados

