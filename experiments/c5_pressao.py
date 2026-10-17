import time
import psutil
import os

def print_memoria(etapa):
    mem = psutil.virtual_memory()
    print(f"[{etapa}] RAM Total: {mem.total/1024**3:.2f} GB | Usada: {mem.used/1024**3:.2f} GB | Livre: {mem.available/1024**3:.2f} GB | {mem.percent}% em uso")

def main():
    print("--- INICIANDO EXPERIMENTO C5: PRESSÃO DE MEMÓRIA ---")
    print_memoria("Inicial")
    
    # Lista para segurar a memória (simula o índice vetorial)
    indice_gigante = []
    
    # Vamos alocar blocos de 500MB por vez
    bloco_mb = 500
    num_blocos = 5 # Total de 2.5GB
    
    for i in range(1, num_blocos + 1):
        print(f"\nAlocando bloco {i} de {bloco_mb} MB...")
        
        # Cria uma lista com números (cada int ocupa memória no Python)
        # Força a alocação real preenchendo com zeros
        bloco = [0] * (bloco_mb * 1024 * 1024 // 8) # /8 por causa do tamanho do ponteiro no Python
        
        indice_gigante.append(bloco)
        
        # Dá um tempo pro SO respirar e atualizar as métricas
        time.sleep(1) 
        print_memoria(f"Após alocar {i*bloco_mb} MB")
    
    print("\n--- PRESSÃO MÁXIMA ATINGIDA ---")
    print("Aguardando 5 segundos para observar o comportamento do SO...")
    time.sleep(5)
    
    print("\nLimpando memória (liberando o índice)...")
    del indice_gigante
    time.sleep(1)
    print_memoria("Após liberação")

if __name__ == "__main__":
    main()
