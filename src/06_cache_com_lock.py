import threading
import time

cache_compartilhado = {}
# O nosso mecanismo de sincronização (Mutex)
lock_cache = threading.Lock() 

def processar_consulta_com_lock(query):
    # AQUISIÇÃO DO LOCK: Apenas uma thread pode passar por aqui por vez
    with lock_cache: 
        if query not in cache_compartilhado:
            time.sleep(0.01) # Simula geração
            cache_compartilhado[query] = "RESPOSTA_GERADA"
            return True # Miss
    # LIBERAÇÃO DO LOCK: O bloco with termina e libera o lock
    return False # Hit

def main():
    print("--- DEMONSTRANDO SOLUÇÃO COM LOCK (MUTEX) ---")
    cache_compartilhado.clear()
    
    query = "como funciona memoria virtual"
    hits = 0
    misses = 0
    threads = []
    
    def worker():
        nonlocal hits, misses
        resultado = processar_consulta_com_lock(query)
        if resultado:
            misses += 1
        else:
            hits += 1

    for _ in range(5):
        t = threading.Thread(target=worker)
        threads.append(t)
        t.start()
        
    for t in threads:
        t.join()
        
    print(f"Tentativas: 5 | Cache Misses (gerou de novo): {misses} | Cache Hits: {hits}")
    
    if misses == 1:
        print("✅ SUCESSO: Apenas 1 thread gerou, as outras aproveitaram o cache!")
    else:
        print("❌ Ainda há concorrência indesejada.")

if __name__ == "__main__":
    main()
