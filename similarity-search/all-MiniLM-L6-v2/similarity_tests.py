#!/usr/bin/env python3
"""
Similarity Tests - Script para testes comparativos de algoritmos de busca por similaridade.

Suporta múltiplos algoritmos (BM25, Cosine, FAISS Cosine, FAISS Euclidean, ChromaDB)
e múltiplos modelos de embeddings.
"""

import json
import re
import time
import tracemalloc
import psutil
import os
from typing import List, Dict, Tuple, Any

# Algoritmos baseados em embeddings
from sentence_transformers import SentenceTransformer, util
import faiss
import chromadb

# BM25
from rank_bm25 import BM25Okapi

# Cache para modelos SentenceTransformer
_model_cache: Dict[str, SentenceTransformer] = {}


# =============================================================================
# CONFIGURAÇÃO
# =============================================================================

# Dataset de entrada
DATASET_FILE = "dataset_credenciais.json"

# Modelos de embeddings para testar
MODELOS = [
    "sentence-transformers/all-MiniLM-L6-v2",
    "paraphrase-multilingual-MiniLM-L12-v2",
    "neuralmind/bert-base-portuguese-cased",
    "BAAI/bge-m3",
]

# Algoritmos baseados em embeddings
ALGORITMOS_EMBEDDING = [
    "cosine",
    "faiss_cosine",
    "faiss_euclidean",
    "chromadb",
]

# =============================================================================
# FUNÇÕES AUXILIARES
# =============================================================================


def carregar_dataset(arquivo: str) -> Dict:
    """Carrega o dataset JSON com base de conhecimento, queries e respostas úteis."""
    with open(arquivo, "r", encoding="utf-8") as f:
        return json.load(f)


def tokenize(text: str) -> List[str]:
    """Tokeniza texto para BM25 (remove pontuação, lower case, split)."""
    return re.sub(r"[^\w\s]", "", text.lower()).split()


def normalizar_nome_colecao(modelo_nome: str) -> str:
    """
    Normaliza o nome do modelo para atender aos requisitos do ChromaDB.
    
    Requisitos:
    - 3-512 caracteres
    - Caracteres permitidos: [a-zA-Z0-9._-]
    - Deve começar e terminar com [a-zA-Z0-9]
    
    Exemplo:
    - Entrada: "sentence-transformers/all-MiniLM-L6-v2"
    - Saída: "sentence-transformers_all-MiniLM-L6-v2"
    """
    # Substituir caracteres inválidos por '_'
    nome_normalizado = re.sub(r"[^a-zA-Z0-9._-]", "_", modelo_nome)
    
    # Garantir que comece com caractere alfanumérico
    if nome_normalizado and not re.match(r"^[a-zA-Z0-9]", nome_normalizado):
        nome_normalizado = "model_" + nome_normalizado
    
    # Garantir que termine com caractere alfanumérico
    if nome_normalizado and not re.match(r".*[a-zA-Z0-9]$", nome_normalizado):
        nome_normalizado = nome_normalizado + "_model"
    
    # Garantir tamanho mínimo (3 caracteres)
    if len(nome_normalizado) < 3:
        nome_normalizado = "model_" + nome_normalizado
    
    # Garantir tamanho máximo (512 caracteres)
    if len(nome_normalizado) > 512:
        nome_normalizado = nome_normalizado[:512]
        # Ajustar final para terminar com caractere alfanumérico
        while nome_normalizado and not re.match(r".*[a-zA-Z0-9]$", nome_normalizado):
            nome_normalizado = nome_normalizado[:-1]
    
    return nome_normalizado


def obter_modelo(modelo_nome: str) -> SentenceTransformer:
    """
    Obtém uma instância de SentenceTransformer com cache.
    
    Evita recarregar o mesmo modelo múltiplas vezes, economizando tempo e memória.
    
    Args:
        modelo_nome: Nome do modelo (ex: "sentence-transformers/all-MiniLM-L6-v2")
    
    Returns:
        Instância de SentenceTransformer carregada ou em cache
    """
    if modelo_nome not in _model_cache:
        print(f"  Carregando modelo: {modelo_nome}")
        _model_cache[modelo_nome] = SentenceTransformer(modelo_nome)
    else:
        print(f"  Usando modelo em cache: {modelo_nome}")
    return _model_cache[modelo_nome]


def calcular_ranks_uteis(
    resultados_ordenados: List[str],
    respostas_uteis_indices: List[int],
    base_conhecimento: List[str],
) -> List[int]:
    """
    Calcula os ranks das respostas úteis.
    Retorna uma lista com a posição (1-based) de cada resposta útil no ranking.
    """
    ranks: list[int] = []
    for idx_util in respostas_uteis_indices:
        doc_util = base_conhecimento[idx_util]
        for pos, doc in enumerate(resultados_ordenados):
            if doc == doc_util:
                ranks.append(pos + 1)  # 1-based
                break
    ranks.sort()
    return ranks


def obter_process_info() -> Tuple[float, float]:
    """Obtém uso de CPU (%) e memória (MB) do processo atual."""
    process = psutil.Process(os.getpid())
    cpu_percent = process.cpu_percent(interval=None)
    mem_info = process.memory_info()
    mem_mb = mem_info.rss / (1024 * 1024)
    return cpu_percent, mem_mb


# =============================================================================
# ALGORITMOS
# =============================================================================


def run_bm25(
    base_conhecimento: List[str], queries: List[str], respostas_uteis: List[List[int]]
) -> Dict:
    """Executa testes com BM25 (algoritmo lexical, não usa embeddings)."""
    resultados = []

    # Tokenização do corpus (setup - não conta no tempo)
    tokenized_corpus = [tokenize(doc) for doc in base_conhecimento]
    bm25 = BM25Okapi(tokenized_corpus)

    # Medição apenas da execução das queries
    tracemalloc.start()
    start_time = time.time()
    cpu_start, mem_start = obter_process_info()

    for query_idx, query in enumerate(queries):
        tokenized_query = tokenize(query)
        top_n = bm25.get_top_n(tokenized_query, base_conhecimento, n=len(base_conhecimento))

        ranks_uteis = calcular_ranks_uteis(top_n, respostas_uteis[query_idx], base_conhecimento)
        resultados.append(ranks_uteis)

    end_time = time.time()
    cpu_end, mem_end = obter_process_info()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return {
        "algoritmo": "BM25",
        "modelo": "N/A (lexical)",
        "ranks_por_query": resultados,
        "tempo_total": end_time - start_time,
        "memoria_peak_mb": peak / (1024 * 1024),
        "cpu_percent": abs(cpu_end - cpu_start),
    }


def run_cosine(
    base_conhecimento: List[str],
    queries: List[str],
    respostas_uteis: List[List[int]],
    modelo_nome: str,
) -> Dict:
    """Executa testes com Similaridade de Cosseno (sentence-transformers)."""
    resultados = []

    # Setup - carregar modelo e gerar embeddings (não conta no tempo)
    model = obter_modelo(modelo_nome)
    embeddings_base = model.encode(base_conhecimento)

    # Medição apenas da execução das queries
    tracemalloc.start()
    start_time = time.time()
    cpu_start, mem_start = obter_process_info()

    for query_idx, query in enumerate(queries):
        embedding_query = model.encode(query)
        scores = util.cos_sim(embedding_query, embeddings_base)[0]

        # Ordenar por score (maior para menor)
        indices_ordenados = sorted(
            range(len(scores)), key=lambda i: scores[i].item(), reverse=True
        )
        resultados_ordenados = [base_conhecimento[i] for i in indices_ordenados]

        ranks_uteis = calcular_ranks_uteis(
            resultados_ordenados, respostas_uteis[query_idx], base_conhecimento
        )
        resultados.append(ranks_uteis)

    end_time = time.time()
    cpu_end, mem_end = obter_process_info()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return {
        "algoritmo": "Cosine Similarity",
        "modelo": modelo_nome,
        "ranks_por_query": resultados,
        "tempo_total": end_time - start_time,
        "memoria_peak_mb": peak / (1024 * 1024),
        "cpu_percent": abs(cpu_end - cpu_start),
    }


def run_faiss_cosine(
    base_conhecimento: List[str],
    queries: List[str],
    respostas_uteis: List[List[int]],
    modelo_nome: str,
) -> Dict:
    """Executa testes com FAISS usando Similaridade de Cosseno (IndexFlatIP)."""
    resultados = []

    # Setup - carregar modelo, gerar embeddings e criar índice (não conta no tempo)
    model = obter_modelo(modelo_nome)
    embeddings = model.encode(base_conhecimento).astype("float32")
    faiss.normalize_L2(embeddings)

    d = embeddings.shape[1]
    index = faiss.IndexFlatIP(d)
    index.add(embeddings)

    # Medição apenas da execução das queries
    tracemalloc.start()
    start_time = time.time()
    cpu_start, mem_start = obter_process_info()

    for query_idx, query in enumerate(queries):
        query_embedding = model.encode([query]).astype("float32")
        faiss.normalize_L2(query_embedding)

        k = len(base_conhecimento)
        scores, indices = index.search(query_embedding, k)

        resultados_ordenados = [base_conhecimento[idx] for idx in indices[0]]
        ranks_uteis = calcular_ranks_uteis(
            resultados_ordenados, respostas_uteis[query_idx], base_conhecimento
        )
        resultados.append(ranks_uteis)

    end_time = time.time()
    cpu_end, mem_end = obter_process_info()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return {
        "algoritmo": "FAISS Cosine",
        "modelo": modelo_nome,
        "ranks_por_query": resultados,
        "tempo_total": end_time - start_time,
        "memoria_peak_mb": peak / (1024 * 1024),
        "cpu_percent": abs(cpu_end - cpu_start),
    }


def run_faiss_euclidean(
    base_conhecimento: List[str],
    queries: List[str],
    respostas_uteis: List[List[int]],
    modelo_nome: str,
) -> Dict:
    """Executa testes com FAISS usando Distância Euclidiana (IndexFlatL2)."""
    resultados = []

    # Setup - carregar modelo, gerar embeddings e criar índice (não conta no tempo)
    model = obter_modelo(modelo_nome)
    embeddings = model.encode(base_conhecimento).astype("float32")

    d = embeddings.shape[1]
    index = faiss.IndexFlatL2(d)
    index.add(embeddings)

    # Medição apenas da execução das queries
    tracemalloc.start()
    start_time = time.time()
    cpu_start, mem_start = obter_process_info()

    for query_idx, query in enumerate(queries):
        query_embedding = model.encode([query]).astype("float32")

        k = len(base_conhecimento)
        distancias, indices = index.search(query_embedding, k)

        resultados_ordenados = [base_conhecimento[idx] for idx in indices[0]]
        ranks_uteis = calcular_ranks_uteis(
            resultados_ordenados, respostas_uteis[query_idx], base_conhecimento
        )
        resultados.append(ranks_uteis)

    end_time = time.time()
    cpu_end, mem_end = obter_process_info()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return {
        "algoritmo": "FAISS Euclidean",
        "modelo": modelo_nome,
        "ranks_por_query": resultados,
        "tempo_total": end_time - start_time,
        "memoria_peak_mb": peak / (1024 * 1024),
        "cpu_percent": abs(cpu_end - cpu_start),
    }


def run_chromadb(
    base_conhecimento: List[str],
    queries: List[str],
    respostas_uteis: List[List[int]],
    modelo_nome: str,
) -> Dict:
    """Executa testes com ChromaDB (usa similaridade de cosseno internamente)."""
    resultados = []

    # Setup - criar cliente, coleção e adicionar documentos (não conta no tempo)
    client = chromadb.Client()
    collection_name = normalizar_nome_colecao(f"teste_collection_{modelo_nome}")
    collection = client.create_collection(name=collection_name)

    model = obter_modelo(modelo_nome)
    embeddings = model.encode(base_conhecimento).tolist()

    ids = [f"id{i}" for i in range(len(base_conhecimento))]
    collection.add(embeddings=embeddings, documents=base_conhecimento, ids=ids)

    # Medição apenas da execução das queries
    tracemalloc.start()
    start_time = time.time()
    cpu_start, mem_start = obter_process_info()

    for query_idx, query in enumerate(queries):
        query_embedding = model.encode([query]).tolist()

        results = collection.query(
            query_embeddings=query_embedding,
            n_results=len(base_conhecimento),
        )

        resultados_ordenados = results["documents"][0]
        ranks_uteis = calcular_ranks_uteis(
            resultados_ordenados, respostas_uteis[query_idx], base_conhecimento
        )
        resultados.append(ranks_uteis)

    end_time = time.time()
    cpu_end, mem_end = obter_process_info()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return {
        "algoritmo": "ChromaDB",
        "modelo": modelo_nome,
        "ranks_por_query": resultados,
        "tempo_total": end_time - start_time,
        "memoria_peak_mb": peak / (1024 * 1024),
        "cpu_percent": abs(cpu_end - cpu_start),
    }


# =============================================================================
# EXECUÇÃO DOS TESTES
# =============================================================================


def executar_todos_testes(dataset: Dict) -> List[Dict]:
    """Executa todos os algoritmos com todos os modelos e coleta métricas."""
    base_conhecimento = dataset["base_conhecimento"]
    queries = dataset["queries"]
    respostas_uteis = dataset["respostas_uteis"]

    todos_resultados = []

    # 1. BM25 (estático, não depende de modelo)
    print("Executando BM25...")
    resultado_bm25 = run_bm25(base_conhecimento, queries, respostas_uteis)
    todos_resultados.append(resultado_bm25)

    # 2. Algoritmos baseados em embeddings
    for modelo in MODELOS:
        print(f"\nExecutando com modelo: {modelo}")

        for algo in ALGORITMOS_EMBEDDING:
            print(f"  -> {algo}...")

            if algo == "cosine":
                resultado = run_cosine(base_conhecimento, queries, respostas_uteis, modelo)
            elif algo == "faiss_cosine":
                resultado = run_faiss_cosine(base_conhecimento, queries, respostas_uteis, modelo)
            elif algo == "faiss_euclidean":
                resultado = run_faiss_euclidean(base_conhecimento, queries, respostas_uteis, modelo)
            elif algo == "chromadb":
                resultado = run_chromadb(base_conhecimento, queries, respostas_uteis, modelo)

            todos_resultados.append(resultado)

    return todos_resultados


# =============================================================================
# GERAÇÃO DO RELATÓRIO
# =============================================================================


def calcular_rank_medio(ranks: List[int]) -> float:
    """Calcula a média dos ranks."""
    if not ranks:
        return 0.0
    return sum(ranks) / len(ranks)


def gerar_relatorio(
    dataset_nome: str, resultados: List[Dict], queries: List[str]
) -> str:
    """Gera o relatório em Markdown com tabela de resultados."""
    linhas = []
    linhas.append("# Relatório de Testes de Similaridade\n")
    linhas.append(f"**Dataset:** {dataset_nome}\n")
    linhas.append(f"**Queries testadas:** {len(queries)}\n")
    linhas.append("")

    # Tabela de resultados detalhada
    linhas.append("## Resultados Detalhados\n")
    linhas.append("")

    # Cabeçalho da tabela
    header = "| Modelo | Algoritmo | "
    for i, query in enumerate(queries):
        header += f"Query {i+1} | "
    header += "Rank Médio | Tempo (s) | CPU (%) | Memória (MB) |"
    linhas.append(header)

    # Separador
    separador = "|--------|-----------|"
    for _ in queries:
        separador += "--------|"
    separador += "-----------|-----------|---------|--------------|"
    linhas.append(separador)

    # Linhas de dados
    for res in resultados:
        linha = f"| {res['modelo']} | {res['algoritmo']} | "

        # Ranks por query
        for ranks_query in res["ranks_por_query"]:
            ranks_str = ", ".join(map(str, ranks_query))
            linha += f"{ranks_str} | "

        # Rank médio geral
        todos_ranks = [r for ranks in res["ranks_por_query"] for r in ranks]
        rank_medio = calcular_rank_medio(todos_ranks)
        linha += f"**{rank_medio:.2f}** | "

        # Métricas de desempenho
        linha += f"{res['tempo_total']:.3f} | {res['cpu_percent']:.1f} | {res['memoria_peak_mb']:.2f} |"

        linhas.append(linha)

    linhas.append("")

    # Tabela consolidada por modelo
    linhas.append("## Consolidado por Modelo\n")
    linhas.append("")

    # Agrupar resultados por modelo
    modelos_dict: Dict[str, List[Dict]] = {}
    for res in resultados:
        modelo = res['modelo']
        if modelo not in modelos_dict:
            modelos_dict[modelo] = []
        modelos_dict[modelo].append(res)

    # Cabeçalho da tabela consolidada
    header_consolidado = "| Modelo | "
    for algo in set(res['algoritmo'] for res in resultados):
        header_consolidado += f"{algo} | "
    header_consolidado += "Média Geral |"
    linhas.append(header_consolidado)

    # Separador
    separador_consolidado = "|--------|"
    for _ in set(res['algoritmo'] for res in resultados):
        separador_consolidado += "--------|"
    separador_consolidado += "-------------|"
    linhas.append(separador_consolidado)

    # Linhas de dados consolidados
    for modelo, res_list in modelos_dict.items():
        linha = f"| {modelo} |"

        # Criar mapa algoritmo -> rank médio
        algo_ranks = {res['algoritmo']: res for res in res_list}

        # Rank médio por algoritmo
        for algo in sorted(set(res['algoritmo'] for res in resultados)):
            if algo in algo_ranks:
                res = algo_ranks[algo]
                todos_ranks = [r for ranks in res["ranks_por_query"] for r in ranks]
                rank_medio = calcular_rank_medio(todos_ranks)
                linha += f" {rank_medio:.2f} |"
            else:
                linha += " - |"

        # Média geral do modelo (todos os algoritmos)
        todos_ranks_modelo = []
        for res in res_list:
            todos_ranks_modelo.extend([r for ranks in res["ranks_por_query"] for r in ranks])
        media_geral = calcular_rank_medio(todos_ranks_modelo)
        linha += f" **{media_geral:.2f}** |"

        linhas.append(linha)

    linhas.append("")

    # Conclusão
    linhas.append("## Conclusão\n")
    linhas.append("")

    # Encontrar o melhor resultado (menor rank médio)
    melhor = min(resultados, key=lambda x: calcular_rank_medio([r for ranks in x["ranks_por_query"] for r in ranks]))
    todos_ranks_melhor = [r for ranks in melhor["ranks_por_query"] for r in ranks]
    melhor_rank_medio = calcular_rank_medio(todos_ranks_melhor)

    linhas.append(
        f"O melhor desempenho foi de **{melhor['algoritmo']}** com modelo **"
        f"{melhor['modelo']}** (rank médio: **{melhor_rank_medio:.2f}**).\n"
    )
    linhas.append("")

    return "\n".join(linhas)


def salvar_relatorio(dataset_nome: str, conteudo: str):
    """Salva o relatório em arquivo Markdown."""
    # Extrair nome base do dataset
    nome_base = os.path.splitext(dataset_nome)[0]
    arquivo_saida = f"{nome_base}_result.md"

    with open(arquivo_saida, "w", encoding="utf-8") as f:
        f.write(conteudo)

    print(f"\nRelatório salvo em: {arquivo_saida}")


# =============================================================================
# MAIN
# =============================================================================


if __name__ == "__main__":
    print("=" * 60)
    print("Similarity Tests - Comparativo de Algoritmos")
    print("=" * 60)

    # Carregar dataset
    print(f"\nCarregando dataset: {DATASET_FILE}")
    dataset = carregar_dataset(DATASET_FILE)

    print(f"Base de conhecimento: {len(dataset['base_conhecimento'])} documentos")
    print(f"Queries: {len(dataset['queries'])}")
    print(f"Respostas úteis por query: {[len(r) for r in dataset['respostas_uteis']]}")

    # Executar testes
    print("\n" + "=" * 60)
    print("Executando testes...")
    print("=" * 60)

    resultados = executar_todos_testes(dataset)

    # Gerar relatório
    print("\n" + "=" * 60)
    print("Gerando relatório...")
    print("=" * 60)

    relatorio = gerar_relatorio(DATASET_FILE, resultados, dataset["queries"])
    salvar_relatorio(DATASET_FILE, relatorio)

    print("\nTestes concluídos!")
