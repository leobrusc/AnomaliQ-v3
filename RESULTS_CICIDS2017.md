# CICIDS2017 Real Benchmark Results

Data: 2026-06-18

## Objetivo

Avaliar deteccao binaria BENIGN vs DDoS no CICIDS2017 real, comparando modelos classicos e QML em protocolo multiseed.

Modelos avaliados:

- Logistic Regression
- Random Forest
- SVM-RBF
- QSVM-ZZ
- QSVM-Pauli
- VQC

Seeds:

```text
42, 123, 2026
```

## Metodologia

Config usado:

```text
configs/cicids_ddos_real_strict.yaml
```

Comando executado:

```powershell
python -m src.experiments.run_cicids2017_benchmark --config configs/cicids_ddos_real_strict.yaml --experiment-name cicids2017_real_benchmark --seeds 42 123 2026
```

O modo strict exige CSVs reais e nao permite fallback sintetico:

```yaml
require_real_dataset: true
fallback_to_synthetic: false
```

O loader CICIDS2017:

- busca CSVs recursivamente em `data/raw/cicids2017/`;
- detecta a coluna `Label` mesmo com espacos no nome original;
- filtra BENIGN vs DDoS;
- remove valores NaN e infinitos;
- mapeia features CICIDS2017 para o contrato tabular do AnomalyQ;
- limita amostras por classe conforme config.

Config experimental relevante:

```yaml
max_samples_per_class: 1000
test_size: 0.3
n_qubits: 4
quantum_max_train: 30
quantum_max_test: 25
vqc_maxiter: 25
```

## Tamanho da base

Perfil completo em:

```text
DATASET_PROFILE_CICIDS2017.md
```

Resumo:

- CSVs analisados: 8
- Linhas totais CICIDS2017: 2,830,743
- Colunas: 79
- BENIGN global: 2,273,097
- DDoS global: 128,027
- Total BENIGN vs DDoS antes do limite: 2,401,124
- Amostras usadas por seed antes do split: ate 2,000

## Artefatos gerados

Diretorio agregado:

```text
results/cicids2017/cicids2017_real_benchmark-aggregate/
```

Arquivos:

- `cicids2017_multiseed_all_metrics.csv`
- `cicids2017_selected_model_metrics.csv`
- `cicids2017_publication_summary.csv`
- `cicids2017_publication_table.md`
- `cicids2017_publication_table.tex`

Figuras:

- `plots/cicids2017_accuracy_publication.png`
- `plots/cicids2017_precision_publication.png`
- `plots/cicids2017_recall_publication.png`
- `plots/cicids2017_f1_publication.png`
- `plots/cicids2017_roc_auc_publication.png`
- `plots/cicids2017_mcc_publication.png`

## Resultados por modelo

| model | accuracy | precision | recall | f1 | roc_auc | mcc |
| --- | --- | --- | --- | --- | --- | --- |
| Logistic Regression | 0.9683 ± 0.0117 | 0.9445 ± 0.0213 | 0.9956 ± 0.0038 | 0.9693 ± 0.0110 | 0.9859 ± 0.0081 | 0.9382 ± 0.0223 |
| Random Forest | 0.9967 ± 0.0017 | 0.9978 ± 0.0019 | 0.9956 ± 0.0038 | 0.9967 ± 0.0017 | 0.9988 ± 0.0021 | 0.9933 ± 0.0033 |
| SVM-RBF | 0.9672 ± 0.0111 | 0.9425 ± 0.0220 | 0.9956 ± 0.0038 | 0.9682 ± 0.0105 | 0.9945 ± 0.0010 | 0.9362 ± 0.0210 |
| QSVM-ZZ | 0.7333 ± 0.1890 | 0.8718 ± 0.2221 | 0.6329 ± 0.1094 | 0.7302 ± 0.1455 | 0.8420 ± 0.1469 | 0.4908 ± 0.4014 |
| QSVM-PAULI | 0.7200 ± 0.2117 | 0.8208 ± 0.2292 | 0.6808 ± 0.0757 | 0.7401 ± 0.1431 | 0.8505 ± 0.1543 | 0.4332 ± 0.4704 |
| VQC | 0.6267 ± 0.1007 | 0.7000 ± 0.1732 | 0.5774 ± 0.0414 | 0.6247 ± 0.0797 | 0.6378 ± 0.1040 | 0.2787 ± 0.2116 |

## Analise dos modelos classicos

Random Forest foi o melhor modelo geral no benchmark inicial, com F1 medio `0.9967` e MCC medio `0.9933`. O desvio padrao baixo indica estabilidade nas tres seeds.

Logistic Regression e SVM-RBF tambem tiveram desempenho alto, com F1 medio acima de `0.968`. Ambos tiveram recall medio `0.9956`, mas precision inferior ao Random Forest, indicando mais falsos positivos relativos.

O resultado sugere que, no subconjunto balanceado de ate 1000 amostras por classe, as features mapeadas do CICIDS2017 carregam sinal suficiente para baselines classicos fortes.

## Analise dos modelos quanticos

QSVM-ZZ e QSVM-Pauli funcionaram no benchmark real usando representacao PCA reduzida para `n_qubits=4`, com apenas `quantum_max_train=30` e `quantum_max_test=25`.

QSVM-Pauli obteve F1 medio `0.7401`, ligeiramente acima do QSVM-ZZ (`0.7302`), mas ambos apresentaram alta variancia entre seeds. O MCC medio ficou abaixo dos baselines classicos, indicando separacao binaria menos confiavel.

VQC teve F1 medio `0.6247` e MCC medio `0.2787`, com desempenho inferior aos QSVMs. O resultado deve ser interpretado com cautela porque o VQC usa poucas amostras, poucas iteracoes e circuito pequeno para manter viabilidade em simulador local.

## Limitacoes

- O benchmark usa `max_samples_per_class=1000`; ainda nao representa a base binaria completa.
- Modelos quanticos usam `quantum_max_train=30` e `quantum_max_test=25`, portanto a comparacao direta com modelos classicos deve ser reportada como limitada por custo de simulacao.
- As features CICIDS2017 foram mapeadas para o contrato comum do AnomalyQ, nao para todo o vetor original de 78 features.
- Nao foi executado teste estatistico formal alem de media/desvio padrao.
- O benchmark foi executado em simulador/local, nao em hardware IBM Quantum.

## Recomendacoes

1. Repetir benchmark com `max_samples_per_class` maior para classicos.
2. Criar protocolo separado para comparacao justa classica vs QML usando exatamente o mesmo subconjunto PCA.
3. Aumentar `quantum_max_train` gradualmente e medir custo/beneficio.
4. Adicionar teste Wilcoxon pareado para SVM-RBF vs Random Forest e QSVM-ZZ vs QSVM-Pauli.
5. Gerar tabelas finais com tempo de treino, tempo de inferencia, profundidade, CNOTs e numero de parametros.
6. Repetir em UNSW-NB15 para avaliar generalizacao.
