# CICIDS2017 Real Benchmark Results

Data: 2026-06-18

## Objetivo

Executar benchmark real BENIGN vs DDoS no CICIDS2017 comparando:

- Logistic Regression
- Random Forest
- SVM-RBF
- QSVM-ZZ
- QSVM-Pauli
- VQC

Metricas planejadas:

- Accuracy
- Precision
- Recall
- F1
- ROC-AUC
- MCC

## Estado da execucao

Status: bloqueado por ausencia dos CSVs reais locais.

Diretorio esperado:

```text
data/raw/cicids2017/*.csv
```

Mensagem strict validada:

```text
CICIDS2017 dataset not found.
Expected CSV files under:
data/raw/cicids2017/*.csv
```

## Infraestrutura implementada

- Config strict: `configs/cicids_ddos_real_strict.yaml`
- Runner dedicado: `src/experiments/run_cicids2017_benchmark.py`
- Agregacao multiseed: seeds `42`, `123`, `2026`
- Metricas publicaveis incluindo MCC
- Exportacao:
  - CSV bruto por seed/modelo
  - CSV agregado
  - tabela Markdown
  - tabela LaTeX
  - figuras PNG

## Comando de benchmark real

```powershell
python -m src.experiments.run_cicids2017_benchmark --config configs/cicids_ddos_real_strict.yaml --experiment-name cicids2017_real_benchmark --seeds 42 123 2026
```

## Saidas esperadas

```text
results/cicids2017/
  cicids2017_real_benchmark-seed-42-<timestamp>/
    metrics.csv
    summary.md
    config_snapshot.yaml
    experiment_manifest.json
    plots/
    artifacts/
  cicids2017_real_benchmark-seed-123-<timestamp>/
  cicids2017_real_benchmark-seed-2026-<timestamp>/
  cicids2017_real_benchmark-aggregate/
    cicids2017_multiseed_all_metrics.csv
    cicids2017_selected_model_metrics.csv
    cicids2017_publication_summary.csv
    cicids2017_publication_table.md
    cicids2017_publication_table.tex
    plots/
      cicids2017_accuracy_publication.png
      cicids2017_precision_publication.png
      cicids2017_recall_publication.png
      cicids2017_f1_publication.png
      cicids2017_roc_auc_publication.png
      cicids2017_mcc_publication.png
```

## Criterios para resultado publicavel

1. Confirmar que os CSVs reais foram carregados sem fallback.
2. Confirmar que cada seed gerou manifest e config snapshot.
3. Confirmar que todos os seis modelos do protocolo produziram metricas.
4. Reportar media e desvio padrao por modelo.
5. Separar metricas classicas de metricas NISQ.
6. Registrar tempo de treino/inferencia e custo de circuito para QSVM/VQC.

## Proximo passo

Copiar os CSVs reais para `data/raw/cicids2017/` e executar o comando de benchmark real strict.
