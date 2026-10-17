import queue
import time
import threading

# Fila super pequena para encher rápido
FILA = queue.Queue(maxsize=3)

def consumidor_lento():
    while True:
        item = FILA.get()
        if item is None:
            FILA.task_done()
            break
        print(f"[Consumidor] Processando {item} (vai demorar 1s)...")
        time.sleep(1) # Simula processamento pesado (ex: LLM)
        FILA.task_done()

def main():
    print("--- INICIANDO C6: FALHA CONTROLADA (FILA SATURADA) ---")
    print(f"Capacidade máxima da fila: {FILA.maxsize}")
    
    # Inicia 1 consumidor lento
    t = threading.Thread(target=consumidor_lento)
    t.start()
    
    # O produtor tenta colocar 6 itens na fila rapidamente
    print("\n[Produtor] Tentando enviar 6 itens rapidamente...")
    for i in range(6):
        try:
            # O non_blocking impede que o produtor fique travado pra sempre. 
            # Se a fila estiver cheia, ele lança a exceção queue.Full
            FILA.put(f"Query_{i}", block=False)
            print(f"[Produtor] Enviou Query_{i}. Tamanho atual da fila: {FILA.qsize()}")
        except queue.Full:
            print(f"❌ [ERRO CONTROLADO] Fila cheia! Não foi possível enfileirar Query_{i}.")
            print("   (No mundo real, o servidor retornaria HTTP 503 - Service Unavailable)")
    
    print("\n[Produtor] Terminou de tentar enviar.")
    
    # Espera o consumidor terminar de limpar a fila
    print("Aguardando o consumidor esvaziar a fila...")
    FILA.join()
    
    # Encerra o consumidor
    FILA.put(None)
    t.join()
    print("\nTeste finalizado com sucesso!")

if __name__ == "__main__":
    main()
