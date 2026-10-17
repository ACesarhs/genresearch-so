# GenResearch-Servidor

Trabalho da disciplina de Sistemas Operacionais (AV2).

## Descrição
Este projeto implementa um serviço simplificado de IA generativa e RAG (Retrieval-Augmented Generation). O foco não é a qualidade textual, mas sim a observação do comportamento do Sistema Operacional (memória, concorrência, filas e caches).

## Ambiente de Execução
- **SO**: Ubuntu 24.04 LTS (VM VirtualBox)
- **Kernel**: 6.8.0-134-generic
- **Processador**: x86_64
- **RAM**: 3.8 GB
- **Swap**: 0 B
- **Linguagem**: Python 3.12
- **Bibliotecas**: psutil, matplotlib, pandas

## Como Reproduzir
1. Clone o repositório.
2. Crie o ambiente virtual: `python3 -m venv .venv`
3. Ative o ambiente: `source .venv/bin/activate`
4. Instale as dependências: `pip install -r requirements.txt` (ou `pip install psutil matplotlib pandas`)
5. Gere o corpus: `python3 experiments/01_gerar_corpus.py`
6. Faça a ingestão: `python3 src/02_ingest.py`
7. Rode os experimentos na pasta `experiments/` ou os servidores na pasta `src/`.

## Estrutura de Pastas
- `src/`: Código principal (ingestão, RAG, fila concorrente, servidor completo).
- `experiments/`: Scripts dos testes C1 a C6 e geração de gráficos.
- `results/`: CSVs e imagens geradas.

## Vídeo de Apresentação
O link do vídeo está no arquivo [VIDEO.md](VIDEO.md).
