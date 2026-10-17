import os
import sqlite3
import random
import time
import hashlib
import struct
import math

DB_PATH = os.path.expanduser("~/genresearch/data/genresearch.db")

def gerar_embedding_simulado(texto, dim=384):
    seed = int(hashlib.md5(texto.encode()).hexdigest(), 16) % (2**32)
    rng = random.Random(seed)
    return [rng.uniform(-1.0, 1.0) for _ in range(dim)]

def similaridade_cosseno(v1, v2):
    dot_product = sum(a * b for a, b in zip(v1, v2))
    norm1 = math.sqrt(sum(a * a for a in v1))
    norm2 = math.sqrt(sum(b * b for b in v2))
    if norm1 == 0 or norm2 == 0: return 0
    return dot_product / (norm1 * norm2)

def recuperar_e_gerar(query):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 1. Gera embedding da query
    query_emb = gerar_embedding_simulado(query)
    
    # 2. Busca todos os documentos do banco (força bruta para simplificar)
    cursor.execute("SELECT filename, content, embedding FROM docs")
    rows = cursor.fetchall()
    conn.close()
    
    # 3. Calcula similaridade
    resultados = []
    for filename, content, emb_bytes in rows:
        # Desempacota o BLOB para lista de floats
        doc_emb = list(struct.unpack(f'384f', emb_bytes))
        score = similaridade_cosseno(query_emb, doc_emb)
        resultados.append((score, filename, content))
    
    # Ordena pelos maiores scores e pega o Top 3
    resultados.sort(key=lambda x: x[0], reverse=True)
    top_3 = resultados[:3]
    
    # 4. Monta o contexto (simulando o que iria para o LLM)
    contexto = "\n".join([f"[{fn}] {cnt[:100]}..." for _, fn, cnt in top_3])
    
    # 5. Simula o tempo de "geração" do LLM (0.2 a 0.5 segundos)
    tempo_geracao = random.uniform(0.2, 0.5)
    time.sleep(tempo_geracao)
    
    resposta = f"Resposta baseada no contexto: {top_3[0][2][:150]}..."
    return contexto, resposta, tempo_geracao

if __name__ == "__main__":
    print("Testando busca e geração para a query: 'memoria virtual e cache'")
    print("-" * 50)
    
    start = time.time()
    contexto, resposta, t_gen = recuperar_e_gerar("memoria virtual e cache")
    total = time.time() - start
    
    print(f"[CONTEXTO RECUPERADO]:\n{contexto}\n")
    print(f"[RESPOSTA GERADA]:\n{resposta}\n")
    print(f"[MÉTRICAS]: Tempo de geração simulado: {t_gen:.2f}s | Tempo total: {total:.2f}s")
