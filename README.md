# AnomaliQ v3

Suíte experimental reprodutível para avaliar detecção adaptativa de ataques DDoS com modelos clássicos, Quantum Machine Learning e POCs híbridas em ambiente NISQ.

## POCs

- **Baseline clássico:** SVM-RBF, Random Forest, Logistic Regression, Isolation Forest, XGBoost quando instalado e Autoencoder clássico simples.
- **QSVM:** `ZZFeatureMap`, `PauliFeatureMap`, `FidelityQuantumKernel` e `QSVC`, comparados com SVM-RBF usando as mesmas features reduzidas por PCA.
- **VQC:** `ZZFeatureMap`, `RealAmplitudes`, histórico de loss e gráfico de convergência. Se `qiskit_algorithms` não estiver instalado, usa fallback variacional clássico e registra a limitação no relatório.
- **QAE:** interface de Quantum Autoencoder com fallback funcional para Autoencoder clássico treinado apenas com tráfego benigno.
- **QAOA:** constrói grafo pequeno de tráfego, formula Max-Cut e salva a partição em `results/artifacts/qaoa_partition.csv`.
- **VQE score:** calcula score Hamiltoniano `H_DDoS = sum_i w_i Z_i + sum_ij J_ij Z_i Z_j` e compara com os rótulos.
- **FALQON drift:** POC funcional de concept drift com janelas temporais e retreino adaptativo; o FALQON completo fica documentado como TODO.
- **Benchmark NISQ:** mede qubits, profundidade, parâmetros, CNOTs, tempos e degradação de F1 sob ruído aproximado. Aer é opcional.

## Instalação

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Dependências opcionais (`qiskit-algorithms`, `qiskit-aer`, `xgboost`, `torch`) não são obrigatórias para a suíte sintética. Quando ausentes, os runners registram fallback ou falha em `results/failures.csv` e continuam.

## Execução

```powershell
python -m src.experiments.run_all --config configs/synthetic.yaml
python -m src.experiments.run_all --config configs/synthetic.yaml --experiment-name synthetic-smoke
python -m src.experiments.run_baselines --config configs/synthetic.yaml
python -m src.experiments.run_qsvm --config configs/synthetic.yaml
python -m src.experiments.run_vqc --config configs/synthetic.yaml
python -m src.experiments.run_vqe --config configs/synthetic.yaml
python -m src.experiments.run_qaoa --config configs/synthetic.yaml
python -m src.experiments.run_falqon --config configs/synthetic.yaml
```

Use `--experiment-name` para prefixar o identificador da execução. Cada execução recebe um sufixo UTC e escreve em um diretório próprio, evitando sobrescrever resultados anteriores.

## Reprodutibilidade e tracking

Os runners criam automaticamente uma árvore de resultados por dataset e execução:

```text
results/
  synthetic/
    synthetic-smoke-20260616T120000Z/
      metrics.csv
      summary.md
      config_snapshot.yaml
      experiment_manifest.json
      plots/
      artifacts/
```

O `experiment_manifest.json` registra:

- hash do commit Git;
- dataset;
- seed;
- número de qubits;
- feature map configurado;
- otimizador;
- timestamp UTC;
- backend detectado.

O `config_snapshot.yaml` salva uma cópia da configuração usada na execução. Isso permite comparar resultados mesmo quando os arquivos em `configs/` forem alterados depois.

## Dataset CICIDS2017

Para modo real, coloque os CSVs em:

```text
data/raw/cicids2017/
```

Os arquivos devem conter uma coluna `Label` com valores `BENIGN` e `DDoS`. Se os CSVs não existirem, o loader emite aviso no `summary.md` e usa automaticamente o dataset sintético HTTP.

Comando:

```powershell
python -m src.experiments.run_all --config configs/cicids_ddos.yaml --experiment-name cicids_initial_benchmark
```

## Dataset UNSW-NB15

Para modo real, coloque os CSVs em:

```text
data/raw/unsw_nb15/
```

O loader aceita coluna binária `label` ou coluna `attack_cat`; tráfego normal vira classe `0` e ataques viram classe `1`. Colunas categóricas são codificadas antes do mapeamento para o contrato comum de features. Se os CSVs não existirem e `fallback_to_synthetic: true`, a execução usa o dataset sintético e registra aviso.

Comando:

```powershell
python -m src.experiments.run_all --config configs/unsw_nb15.yaml --experiment-name unsw_initial_benchmark
```

## Múltiplas Seeds

Para avaliação estatística inicial:

```powershell
python -m src.experiments.run_multiseed --config configs/synthetic.yaml --experiment-name synthetic_multiseed --seeds 42 123 2026
```

O agregado é salvo em `results/<dataset>/<experiment-name>-aggregate/`. Para publicação, use média/desvio padrão e testes pareados como Wilcoxon; para múltiplos modelos, use Friedman.

## Interpretação

- `metrics.csv` mistura modelos classificatórios e POCs não classificatórias; linhas como QAOA podem ter campos de classificação vazios.
- VQE produz score contínuo; métricas supervisionadas só são comparáveis quando o score é convertido em rótulo por threshold.
- QSVM/VQC usam subconjuntos pequenos por custo de simulação.
- QAE e FALQON ainda são POCs/placeholder funcionais.

## Saídas

- `results/<dataset>/<experiment_id>/metrics.csv`: métricas de classificação, mitigação e NISQ.
- `results/<dataset>/<experiment_id>/failures.csv`: experimentos pulados ou quebrados por dependência ausente, quando houver falhas.
- `results/<dataset>/<experiment_id>/summary.md`: relatório automático com limitações.
- `results/<dataset>/<experiment_id>/config_snapshot.yaml`: configuração congelada.
- `results/<dataset>/<experiment_id>/experiment_manifest.json`: manifesto de reprodutibilidade.
- `results/<dataset>/<experiment_id>/plots/f1_comparison.png`
- `results/<dataset>/<experiment_id>/plots/roc_auc_comparison.png`
- `results/<dataset>/<experiment_id>/plots/vqc_convergence.png`
- `results/<dataset>/<experiment_id>/plots/confusion_matrix.png`
- `results/<dataset>/<experiment_id>/plots/nisq_noise_degradation.png`
- `results/<dataset>/<experiment_id>/plots/falqon_drift.png`

## Estrutura

```text
configs/
data/
  raw/
  processed/
src/
  data/
  classical/
  quantum/
  evaluation/
  experiments/
results/
  plots/
  artifacts/
```
