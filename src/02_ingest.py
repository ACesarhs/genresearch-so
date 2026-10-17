import os
import sqlite3
import random
import time
import hashlib

CORPUS_DIR = os.path.expanduser("~/genresearch/data/corpus")
DB_PATH = os.path.expanduser("~/genresearch/data/genresearch.db")

def gerar_embedding_simulado(texto, dim=384):
    """Gera um vetor simulado baseado no hash do texto."""
    # Usa o hash do texto como seed para gerar números "aleatórios" mas determinísticos
    seed = int(hashlib.md5(texto.encode()).hexdigest(), 16) % (2**32)
    rng = random.Random(seed)
    # Cria um vetor de 384 dimensões com valores entre -1 e 1
    return [rng.uniform(-1.0, 1.0) for _ in range(dim)]

def main():
    print(f"Iniciando ingestão do corpus em: {DB_PATH}")
    
    # Conecta ao SQLite
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Cria a tabela de documentos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS docs (
            id INTEGER PRIMARY KEY,
            filename TEXT,
            content TEXT,
            embedding BLOB,
            embedding_dim INTEGER
        )
    ''')
    
    # Limpa a tabela se já existir
    cursor.execute("DELETE FROM docs")
    
    start_time = time.time()
    arquivos = [f for f in os.listdir(CORPUS_DIR) if f.endswith('.txt')]
    
    # Processa cada arquivo
    for idx, filename in enumerate(arquivos):
        caminho = os.path.join(CORPUS_DIR, filename)
        
        with open(caminho, "r", encoding="utf-8") as f:
            conteudo = f.read()
        
        # Gera o embedding simulado
        emb = gerar_embedding_simulado(conteudo)
        
        # Converte a lista de floats para bytes (armazenamento BLOB)
        import struct
        emb_bytes = struct.pack(f'{len(emb)}f', *emb)
        
        # Insere no banco
        cursor.execute(
            "INSERT INTO docs (filename, content, embedding, embedding_dim) VALUES (?, ?, ?, ?)",
            (filename, conteudo, emb_bytes, len(emb))
        )
        
        if (idx + 1) % 100 == 0:
            print(f"  {idx + 1} arquivos processados...")
    
    conn.commit()
    conn.close()
    
    end_time = time.time()
    print(f"Ingestão concluída em {end_time - start_time:.2f} segundos.")

if __name__ == "__main__":
    main()
