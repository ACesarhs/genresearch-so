import pandas as pd
import matplotlib.pyplot as plt
import os

RESULTS_DIR = os.path.expanduser("~/genresearch/results")
CSV_PATH = os.path.join(RESULTS_DIR, "resultados_c1_c2.csv")

# Lê os dados do CSV que geramos no benchmark
df = pd.read_csv(CSV_PATH)

# Gráfico 1: Comparação de Tempo (C1 vs C2)
plt.figure(figsize=(8, 5))
c1_tempos = df[df['metodo'] == 'C1_convencional']['tempo_s']
c2_tempos = df[df['metodo'] == 'C2_mmap']['tempo_s']

plt.bar(['C1 (Convencional)', 'C2 (mmap)'], [c1_tempos.mean(), c2_tempos.mean()], color=['blue', 'green'])
plt.ylabel('Tempo Médio (segundos)')
plt.title('Comparação de Tempo: Leitura Convencional vs mmap')
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Salva o gráfico em PNG
grafico1_path = os.path.join(RESULTS_DIR, "grafico_tempo_mmap.png")
plt.savefig(grafico1_path)
print(f"Gráfico 1 salvo em: {grafico1_path}")

# Gráfico 2: Linha do tempo (Rodadas)
plt.figure(figsize=(8, 5))
plt.plot(c1_tempos.index + 1, c1_tempos, marker='o', label='C1 (Convencional)', color='blue')
plt.plot(c2_tempos.index + 1, c2_tempos, marker='s', label='C2 (mmap)', color='green')
plt.xlabel('Rodada')
plt.ylabel('Tempo (segundos)')
plt.title('Variação de Tempo por Rodada')
plt.xticks([1, 2, 3])
plt.legend()
plt.grid(True, linestyle='--', alpha=0.7)

grafico2_path = os.path.join(RESULTS_DIR, "grafico_rodadas.png")
plt.savefig(grafico2_path)
print(f"Gráfico 2 salvo em: {grafico2_path}")

print("Gráficos gerados com sucesso!")
