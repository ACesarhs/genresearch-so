import os
import time
import mmap
import psutil

# Vamos ler os arquivos do nosso corpus
CORPUS_DIR = os.path.expanduser("~/genresearch/data/corpus")

def medir_memoria():
    process = psutil.Process(os.getpid())
    # RSS = Memória Física Real usada pelo processo
    # VMS = Memória Virtual total alocada
    return process.memory_info().rss / (1024 * 1024), process.memory_info().vms / (1024 * 1024)

def leitura_convencional(arquivos):
    print("\n--- INICIANDO C1: LEITURA CONVENCIONAL (open/read) ---")
    rss_inicial, vms_inicial = medir_memoria()
    print(f"Memória Inicial -> RSS: {rss_inicial:.2f} MB | VMS: {vms_inicial:.2f} MB")
    
    start_time = time.time()
    total_bytes = 0
    
    for filepath in arquivos:
        with open(filepath, "rb") as f:
            while True:
                chunk = f.read(8192) # Lê em blocos de 8KB (buffer)
                if not chunk:
                    break
                total_bytes += len(chunk)
                
    end_time = time.time()
    rss_final, vms_final = medir_memoria()
    
    print(f"Lidos: {total_bytes / 1024:.2f} KB em {end_time - start_time:.4f} segundos")
    print(f"Memória Final   -> RSS: {rss_final:.2f} MB | VMS: {vms_final:.2f} MB")
    print(f"Variação        -> RSS: +{rss_final - rss_inicial:.2f} MB | VMS: +{vms_final - vms_inicial:.2f} MB")

def leitura_mmap(arquivos):
    print("\n--- INICIANDO C2: LEITURA POR MMAP ---")
    rss_inicial, vms_inicial = medir_memoria()
    print(f"Memória Inicial -> RSS: {rss_inicial:.2f} MB | VMS: {vms_inicial:.2f} MB")
    
    start_time = time.time()
    total_bytes = 0
    
    for filepath in arquivos:
        with open(filepath, "rb") as f:
            # Mapeia o arquivo inteiro na memória virtual
            with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mm:
                # Acessa o mapa (simula a leitura)
                total_bytes += len(mm)
                # _ = mm[:] # Se quiser ler tudo de fato
                
    end_time = time.time()
    rss_final, vms_final = medir_memoria()
    
    print(f"Mapeados: {total_bytes / 1024:.2f} KB em {end_time - start_time:.4f} segundos")
    print(f"Memória Final   -> RSS: {rss_final:.2f} MB | VMS: {vms_final:.2f} MB")
    print(f"Variação        -> RSS: +{rss_final - rss_inicial:.2f} MB | VMS: +{vms_final - vms_inicial:.2f} MB")

def main():
    # Pega todos os arquivos .txt do corpus
    arquivos = [os.path.join(CORPUS_DIR, f) for f in os.listdir(CORPUS_DIR) if f.endswith('.txt')]
    print(f"Total de arquivos no corpus: {len(arquivos)}")
    
    # Roda os dois métodos
    leitura_convencional(arquivos)
    time.sleep(1) # Dá um tempo pro SO limpar o cache entre testes
    leitura_mmap(arquivos)

if __name__ == "__main__":
    main()
