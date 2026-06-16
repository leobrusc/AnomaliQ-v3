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
python -m src.experiments.run_baselines --config configs/synthetic.yaml
python -m src.experiments.run_qsvm --config configs/synthetic.yaml
python -m src.experiments.run_vqc --config configs/synthetic.yaml
python -m src.experiments.run_vqe --config configs/synthetic.yaml
python -m src.experiments.run_qaoa --config configs/synthetic.yaml
python -m src.experiments.run_falqon --config configs/synthetic.yaml
```

Use `--reset` nos runners isolados para limpar `metrics.csv`, `failures.csv` e `summary.md` antes de uma execução.

## Dataset CICIDS2017

Para modo real, coloque os CSVs em:

```text
data/raw/cicids2017/
```

Os arquivos devem conter uma coluna `Label` com valores `BENIGN` e `DDoS`. Se os CSVs não existirem, o loader emite aviso no `summary.md` e usa automaticamente o dataset sintético HTTP.

## Saídas

- `results/metrics.csv`: métricas de classificação, mitigação e NISQ.
- `results/failures.csv`: experimentos pulados ou quebrados por dependência ausente.
- `results/summary.md`: relatório automático com limitações.
- `results/plots/f1_comparison.png`
- `results/plots/roc_auc_comparison.png`
- `results/plots/vqc_convergence.png`
- `results/plots/confusion_matrix.png`
- `results/plots/nisq_noise_degradation.png`
- `results/plots/falqon_drift.png`

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
