import os
import random
import string

# Configurações
CORPUS_DIR = os.path.expanduser("~/genresearch/data/corpus")
NUM_ARQUIVOS = 500
TAMANHO_APROX_BYTES = 2048  # ~2KB por arquivo (total ~1MB)

# Vocabulário sintético
palavras = ["sistema", "operacional", "memoria", "virtual", "processo", "thread", 
            "cache", "disco", "arquivo", "rede", "ia", "generativa", "rag", "contexto",
            "vetor", "embedding", "fila", "sincronizacao", "mutex", "deadlock"]

def gerar_texto(num_palavras):
    return " ".join(random.choices(palavras, k=num_palavras))

def main():
    os.makedirs(CORPUS_DIR, exist_ok=True)
    print(f"Gerando {NUM_ARQUIVOS} arquivos em {CORPUS_DIR}...")
    
    for i in range(NUM_ARQUIVOS):
        # Aproximadamente 300 palavras geram ~2KB
        texto = gerar_texto(300)
        caminho = os.path.join(CORPUS_DIR, f"doc_{i:04d}.txt")
        
        with open(caminho, "w", encoding="utf-8") as f:
            f.write(f"Documento {i}\n\n")
            f.write(texto)
            
    print("Concluído!")

if __name__ == "__main__":
    main()
