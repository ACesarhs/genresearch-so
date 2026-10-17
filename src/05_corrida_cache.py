import threading
import time
import random

# Dicionário que será acessado por várias threads
cache_compartilhado = {}
def processar_consulta_sem_lock(query):
    # Simula uma condição de corrida (Race Condition)
    # Se a query não está no cache, o worker vai gerar e salvar.
    if query not in cache_compartilhado:
        # Simula o tempo de geração do LLM (isso causa a troca de contexto entre threads)
        time.sleep(0.01) 
        
        # Threads concorrentes chegam aqui ao mesmo tempo, pois nenhuma colocou no cache ainda
        cache_compartilhado[query] = "RESPOSTA_GERADA"
        
        # Retorna True para indicar que gerou (Cache Miss)
        return True 
    return False # Cache Hit

def main():
    print("--- DEMONSTRANDO RACE CONDITION (SEM LOCK) ---")
    cache_compartilhado.clear()
    
    # Vamos disparar 5 threads para a MESMA query ao mesmo tempo
    query = "como funciona memoria virtual"
    hits = 0
    misses = 0
    
    threads = []
    
    # Função que a thread vai rodar
    def worker():
        nonlocal hits, misses
        resultado = processar_consulta_sem_lock(query)
        if resultado:
            misses += 1
        else:
            hits += 1

    # Dispara 5 threads
    for _ in range(5):
        t = threading.Thread(target=worker)
        threads.append(t)
        t.start()
        
    for t in threads:
        t.join()
        
    print(f"Tentativas: 5 | Cache Misses (gerou de novo): {misses} | Cache Hits: {hits}")
    
    if misses > 1:
        print("❌ FALHA DETECTADA: A mesma query foi gerada várias vezes por falta de lock!")
    else:
        print("✅ SUCESSO: Apenas 1 thread gerou, as outras aproveitaram o cache.")

if __name__ == "__main__":
    main()
