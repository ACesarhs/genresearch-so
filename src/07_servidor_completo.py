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
FILA = queue.Queue(maxsize=20)
NUM_WORKERS = 4
NUM_QUERIES = 50
QUERIES_REPETIDAS = ["memoria", "cache", "deadlock", "ia"] # Queries que vão se repetir

# Estatísticas globais (protegidas por lock)
lock_stats = threading.Lock()
stats = {"hits": 0, "misses": 0, "processados": 0}
cache_compartilhado = {}
lock_cache = threading.Lock()

def gerar_embedding_simulado(texto, dim=384):
    seed = int(hashlib.md5(texto.encode()).hexdigest(), 16) % (2**32)
    rng = random.Random(seed)
    return [rng.uniform(-1.0, 1.0) for _ in range(dim)]

def similaridade_cosseno(v1, v2):
    dot = sum(a * b for a, b in zip(v1, v2))
    n1 = math.sqrt(sum(a * a for a in v1))
    n2 = math.sqrt(sum(b * b for b in v2))
    return dot / (n1 * n2) if n1 and n2 else 0

def worker(worker_id):
    while True:
        item = FILA.get()
        if item is None: 
            FILA.task_done()
            break
            
        query_id, query_texto = item
        
        # --- LÓGICA DE CACHE COM LOCK ---
        with lock_cache:
            if query_texto in cache_compartilhado:
                with lock_stats:
                    stats["hits"] += 1
                FILA.task_done()
                continue # Cache Hit, pula a geração pesada
            else:
                with lock_stats:
                    stats["misses"] += 1
                # Simula o tempo de busca no banco e geração
                time.sleep(random.uniform(0.05, 0.15))
                cache_compartilhado[query_texto] = True
                
        with lock_stats:
            stats["processados"] += 1
            
        FILA.task_done()

def produtor(produtor_id):
    for i in range(NUM_QUERIES // 2): # 2 produtores -> 25 cada
        # 70% de chance de ser uma query repetida (para testar o cache)
        if random.random() < 0.7:
            query = random.choice(QUERIES_REPETIDAS)
        else:
            query = f"query_unica_{produtor_id}_{i}"
            
        query_id = f"P{produtor_id}_Q{i}"
        
        # Bloqueia se a fila estiver cheia
        FILA.put((query_id, query))
        time.sleep(random.uniform(0.01, 0.03))

def main():
    print(f"Iniciando servidor: {NUM_WORKERS} workers, Fila max: {FILA.maxsize}")
    start_global = time.time()
    
    workers = []
    for i in range(NUM_WORKERS):
        t = threading.Thread(target=worker, args=(i,))
        t.start()
        workers.append(t)
        
    producers = []
    for i in range(2):
        t = threading.Thread(target=produtor, args=(i,))
        t.start()
        producers.append(t)
        
    for t in producers: t.join()
    FILA.join()
    
    for _ in range(NUM_WORKERS):
        FILA.put(None)
    for t in workers: t.join()
    
    tempo_total = time.time() - start_global
    print("-" * 50)
    print(f"Tempo total: {tempo_total:.2f}s")
    print(f"Total processado: {stats['processados']} (Misses)")
    print(f"Total Cache Hits: {stats['hits']}")
    print(f"Taxa de Acerto (Hit Rate): {(stats['hits']/(stats['hits']+stats['misses']))*100:.1f}%")

if __name__ == "__main__":
    main()
