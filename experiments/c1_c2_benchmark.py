import os
import time
import mmap
import psutil
import csv
import statistics

CORPUS_DIR = os.path.expanduser("~/genresearch/data/corpus")
RESULTS_DIR = os.path.expanduser("~/genresearch/results")
CSV_PATH = os.path.join(RESULTS_DIR, "resultados_c1_c2.csv")

def get_memoria_mb():
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / (1024 * 1024)

def rodar_leitura_convencional(arquivos):
    start = time.time()
    total_bytes = 0
    for filepath in arquivos:
        with open(filepath, "rb") as f:
            while True:
                chunk = f.read(8192)
                if not chunk: break
                total_bytes += len(chunk)
    return time.time() - start, total_bytes

def rodar_mmap(arquivos):
    start = time.time()
    total_bytes = 0
    for filepath in arquivos:
        with open(filepath, "rb") as f:
            with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mm:
                total_bytes += len(mm)
    return time.time() - start, total_bytes

def main():
    arquivos = [os.path.join(CORPUS_DIR, f) for f in os.listdir(CORPUS_DIR) if f.endswith('.txt')]
    
    resultados = []
    
    print("Iniciando benchmark (3 repetições)...")
    for i in range(1, 4):
        print(f"--- Rodada {i} ---")
        
        # C1
        tempo_c1, bytes_c1 = rodar_leitura_convencional(arquivos)
        mem_c1 = get_memoria_mb()
        resultados.append({"rodada": i, "metodo": "C1_convencional", "tempo_s": round(tempo_c1, 4), "memoria_mb": round(mem_c1, 2)})
        print(f"C1: {tempo_c1:.4f}s | RAM: {mem_c1:.2f} MB")
        
        # C2
        tempo_c2, bytes_c2 = rodar_mmap(arquivos)
        mem_c2 = get_memoria_mb()
        resultados.append({"rodada": i, "metodo": "C2_mmap", "tempo_s": round(tempo_c2, 4), "memoria_mb": round(mem_c2, 2)})
        print(f"C2: {tempo_c2:.4f}s | RAM: {mem_c2:.2f} MB")
    
    # Salva no CSV
    os.makedirs(RESULTS_DIR, exist_ok=True)
    with open(CSV_PATH, mode='w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["rodada", "metodo", "tempo_s", "memoria_mb"])
        writer.writeheader()
        writer.writerows(resultados)
        
    print(f"\nBenchmark concluído! Dados salvos em {CSV_PATH}")

if __name__ == "__main__":
    main()
