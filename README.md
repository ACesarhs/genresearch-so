# 🧠 GenResearch-Servidor: Simulação de RAG e Análise de Sistemas Operacionais

![Python](https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python&logoColor=white)
![Ubuntu](https://img.shields.io/badge/Ubuntu-24.04-E95420?style=for-the-badge&logo=ubuntu&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)

Este repositório contém a implementação do **GenResearch-Servidor**, um serviço simplificado de IA generativa e RAG (Retrieval-Augmented Generation). 

O foco principal do projeto **não é a qualidade da resposta**, mas sim a observação empírica de como o **Sistema Operacional (Linux)** gerencia recursos (memória principal, memória virtual, armazenamento, concorrência, caches e filas) sob uma carga de trabalho inspirada em IA.

## 📋 Sumário
- [Arquitetura do Projeto](#-arquitetura-do-projeto)
- [Ambiente de Execução](#-ambiente-de-execução)
- [Como Reproduzir](#-como-reproduzir)
- [Experimentos Realizados](#-experimentos-realizados)
- [Resultados e Métricas](#-resultados-e-métricas)
- [Vídeo de Apresentação](#-vídeo-de-apresentação)

---

## 🏗️ Arquitetura do Projeto

O sistema simula um pipeline completo de RAG, dividido nas seguintes etapas:
1. **Ingestão**: Lê arquivos `.txt` e gera *embeddings* simulados (vetores de 384 dimensões).
2. **Armazenamento**: Persiste o texto e os vetores em um banco de dados SQLite local.
3. **Fila Concorrente**: Utiliza `queue.Queue` para gerenciar requisições de múltiplos produtores e consumidores.
4. **Recuperação**: Calcula a similaridade de cosseno entre a query e os documentos (força bruta).
5. **Cache Compartilhado**: Armazena respostas recentes em um dicionário protegido por `threading.Lock` (Mutex) para evitar condições de corrida.
6. **Geração Simulada**: Uso de `time.sleep` para simular o custo computacional de um LLM real.

### 📂 Estrutura de Pastas

genresearch/
├── src/
│   ├── 02_ingest.py               # Ingestão e criação do SQLite
│   ├── 03_retrieve_generate.py    # Teste inicial de busca e geração
│   ├── 04_fila_concorrencia.py    # Fila com 2 produtores e 2 consumidores
│   ├── 05_corrida_cache.py        # Demonstração de Race Condition (sem lock)
│   ├── 06_cache_com_lock.py       # Correção da corrida usando Mutex
│   └── 07_servidor_completo.py    # Simulação de carga massiva com 4 workers
├── experiments/
│   ├── 01_gerar_corpus.py         # Gera 500 documentos sintéticos (~2MB)
│   ├── c1_c2_memoria.py           # Leitura convencional vs mmap
│   ├── c1_c2_benchmark.py         # 3 repetições gerando CSV
│   ├── c5_pressao.py              # Estresse de memória (OOM Killer)
│   ├── c6_fila_saturada.py        # Falha controlada (Queue Full)
│   └── 08_gerar_graficos.py       # Gera os gráficos em PNG
├── results/                       # CSVs e gráficos gerados
└── data/                          # Banco SQLite e corpus (ignorados no git)

## 💻 Ambiente de Execução

Os experimentos foram executados em uma Máquina Virtual com as seguintes especificações:
- **Distribuição**: Ubuntu 24.04.4 LTS (Noble Numbat)
- **Kernel**: Linux 6.8.0-134-generic
- **Processador**: x86_64 (VirtualBox)
- **Memória RAM**: 3.82 GB
- **Swap**: 0 B (Sem swap configurado)
- **Linguagem**: Python 3.12
- **Bibliotecas**: `psutil`, `pandas`, `matplotlib`

---

## 🚀 Como Reproduzir

1. Clone o repositório:
   `git clone https://github.com/ACesarhs/genresearch-so.git`
   `cd genresearch-so`

2. Crie e ative o ambiente virtual:
   `python3 -m venv .venv`
   `source .venv/bin/activate`

3. Instale as dependências:
   `pip install -r requirements.txt`

4. Gere o corpus sintético e faça a ingestão:
   `python3 experiments/01_gerar_corpus.py`
   `python3 src/02_ingest.py`

5. Execute os experimentos (dentro do venv):
   `python3 experiments/c1_c2_benchmark.py`
   `python3 src/07_servidor_completo.py`
   `python3 experiments/c5_pressao.py`

---

## 🧪 Experimentos Realizados

| Código | Descrição | Objetivo no SO |
| :--- | :--- | :--- |
| **C1 vs C2** | Leitura `open/read` vs `mmap` | Comparar E/S de disco e cache de páginas. |
| **C3** | Fila concorrente (2 prod, 2 cons) | Avaliar vazão e sincronização de threads. |
| **C4** | Servidor completo (4 workers) | Medir taxa de acerto do cache (Hit Rate). |
| **C5** | Alocação massiva de RAM | Demonstrar pressão de memória e atuação do OOM Killer. |
| **C6** | Fila limitada (maxsize=3) | Demonstrar falha controlada (`queue.Full` / HTTP 503). |

---

## 📊 Resultados e Métricas

Alguns dos resultados extraídos durante os testes (detalhes no relatório final):

- **mmap vs Leitura Convencional**: O `mmap` foi até **4x mais rápido** em leituras a quente (devido ao cache de páginas do Linux).
- **Cache Hit Rate**: Em uma carga de 50 requisições (onde 70% eram repetidas), o cache atingiu **56% de acerto**, economizando processamento e tempo de "geração".
- **Pressão de Memória**: Ao tentar alocar 2.5 GB em uma VM de 3.8 GB sem swap, o processo Python foi encerrado abruptamente pelo **OOM Killer** do kernel Linux no 5º bloco de alocação.
- **Fila Saturada**: O uso de `queue.Queue(maxsize)` com `block=False` evitou que o servidor travasse, retornando falhas rápidas e controladas (HTTP 503).

---

## 🎥 Vídeo de Apresentação

O vídeo demonstrando a execução do projeto e a análise dos resultados pode ser acessado no link abaixo:
🔗 **[Google Drive - Vídeo de Apresentação](https://drive.google.com/drive/folders/1zkfz2-eN6uBYdB3xyeX6NW7xk8szKEYF?usp=sharing)**


---
*Desenvolvido como requisito de avaliação (AV2) para a disciplina de Sistemas Operacionais.*
