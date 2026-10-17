import os
import sqlite3
import random
import time
import hashlib
import struct
import math
import threading
import queue

DB_PATH = os.path.expanduser("~/genresearch/data/genresearch.db")
fila_requisicoes = queue.Queue(maxsize=10) # Fila limitada a 10 itens (Buffer limitado)
NUM_WORKERS = 2
NUM_PRODUTORES = 2
QUERIES_POR_PRODUTOR = 5

lock_resultados = threading.Lock()
resultados_processados = []

def gerar_embedding_simulado(texto, dim=384):
    seed = int(hashlib.md5(texto.encode()).hexdigest(), 16) % (2**32)
    rng = random.Random(seed)
    return [rng.uniform(-1.0, 1.0) for _ in range(dim)]

def similaridade_cosseno(v1, v2):
    dot_product = sum(a * b for a, b in zip(v1, v2))
    norm1 = math.sqrt(sum(a * a for a in v1))
    norm2 = math.sqrt(sum(b * b for b in v2))
    return dot_product / (norm1 * norm2) if norm1 and norm2 else 0

def processo_consumidor(worker_id):
    print(f"[Consumer {worker_id}] Iniciado.")
    while True:
        item = fila_requisicoes.get()
        if item is None: # Sinal de parada (Poison pill)
            fila_requisicoes.task_done()
            break
            
        query_id, query_texto = item
        start = time.time()
        
        # --- SIMULA O RAG ---
        # 1. Busca no banco
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        query_emb = gerar_embedding_simulado(query_texto)
        cursor.execute("SELECT filename, content, embedding FROM docs")
        rows = cursor.fetchall()
        conn.close()
        
        resultados = []
        for filename, content, emb_bytes in rows:
            doc_emb = list(struct.unpack(f'384f', emb_bytes))
            score = similaridade_cosseno(query_emb, doc_emb)
            resultados.append((score, filename))
            
        resultados.sort(key=lambda x: x[0], reverse=True)
        top_doc = resultados[0][1]
        
        # 2. Simula tempo de geração
        time.sleep(random.uniform(0.1, 0.3))
        
        tempo_total = time.time() - start
        
        with lock_resultados:
            resultados_processados.append((query_id, worker_id, top_doc, tempo_total))
            print(f"[Worker {worker_id}] Processou {query_id} -> Doc: {top_doc} ({tempo_total:.2f}s)")
        
        fila_requisicoes.task_done()

def processo_produtor(produtor_id):
    for i in range(QUERIES_POR_PRODUTOR):
        query_id = f"P{produtor_id}_Q{i}"
        query_texto = f"busca {random.choice(['memoria', 'ia', 'cache', 'fila'])}"
        fila_requisicoes.put((query_id, query_texto))
        print(f"[Produtor {produtor_id}] Enfileirou {query_id}")
        time.sleep(random.uniform(0.05, 0.15))

def main():
    print(f"Iniciando {NUM_PRODUTORES} produtores e {NUM_WORKERS} consumidores...")
    print(f"Capacidade max da fila: {fila_requisicoes.maxsize}")
    print("-" * 50)
    
    start_global = time.time()
    
    threads_consumers = []
    for i in range(NUM_WORKERS):
        t = threading.Thread(target=processo_consumidor, args=(i,))
        t.start()
        threads_consumers.append(t)
        
    threads_producers = []
    for i in range(NUM_PRODUTORES):
        t = threading.Thread(target=processo_produtor, args=(i,))
        t.start()
        threads_producers.append(t)
        
    for t in threads_producers: t.join()
    fila_requisicoes.join() # Espera a fila esvaziar
    
    # Envia poison pill para matar os consumidores
    for _ in range(NUM_WORKERS):
        fila_requisicoes.put(None)
        
    for t in threads_consumers: t.join()
    
    tempo_total = time.time() - start_global
    print("-" * 50)
    print(f"Concluído em {tempo_total:.2f}s. Total processado: {len(resultados_processados)}")

if __name__ == "__main__":
    main()
