# Multiseed Validation

Data: 2026-06-18

## Comando executado

```powershell
python -m src.experiments.run_multiseed --config configs/synthetic.yaml --experiment-name multiseed_validation
```

## Resultado

Status: passou apos correcao de robustez na geracao da matriz de confusao.

O primeiro teste falhou na seed `123` porque `finish()` escolhia a melhor linha por F1 sem verificar se `confusion_matrix` existia. A linha `FALQON Drift POC` tinha F1 agregado alto, mas nao possui matriz de confusao supervisionada. A correcao limita o plot da matriz de confusao a linhas com matriz valida, sem alterar a logica dos algoritmos.

Validacao adicional:

```powershell
python -m compileall src legacy
```

Status: passou.

## Artefatos gerados

```text
results/synthetic/multiseed_validation-aggregate/multiseed_all_metrics.csv
results/synthetic/multiseed_validation-aggregate/multiseed_summary.csv
```

## Resumo agregado sintetico

| Modelo | F1 medio | F1 std | ROC-AUC medio | ROC-AUC std |
|---|---:|---:|---:|---:|
| FALQON Drift POC | 0.9868 | 0.0067 | n/a | n/a |
| SVM-RBF | 0.9759 | 0.0143 | 0.9991 | 0.0009 |
| Logistic Regression | 0.9707 | 0.0170 | 0.9990 | 0.0014 |
| Random Forest | 0.9700 | 0.0207 | 0.9978 | 0.0032 |
| SVM-RBF PCA baseline | 0.9548 | 0.0402 | 1.0000 | 0.0000 |
| Isolation Forest | 0.9471 | 0.0242 | 0.9898 | 0.0106 |
| Classical Autoencoder | 0.8966 | 0.0474 | 0.9755 | 0.0111 |
| QAE interface (classical AE fallback) | 0.8966 | 0.0474 | 0.9755 | 0.0111 |
| NISQ noise benchmark | 0.6490 | 0.0711 | n/a | n/a |
| VQC | 0.5242 | 0.1237 | 0.5958 | 0.1557 |
| QSVM-PAULI | 0.4901 | 0.2163 | 0.7749 | 0.1241 |
| QSVM-ZZ | 0.4245 | 0.1245 | 0.7044 | 0.0284 |
| VQE Hamiltonian Score | 0.3803 | 0.1248 | 0.4250 | 0.0442 |
| QAOA MaxCut POC | n/a | n/a | n/a | n/a |

## Interpretacao

- Os baselines classicos continuam fortes no dataset sintetico.
- O SVM-RBF PCA baseline e a comparacao mais justa contra QSVM, pois ambos usam features reduzidas.
- QSVM e VQC funcionam, mas ainda apresentam alta variancia e desempenho inferior no sintetico atual.
- VQE Score esta operacional com threshold, mas deve ser tratado como score continuo convertido para label.
- FALQON e QAOA devem permanecer em grupo separado de POCs, nao no ranking principal de classificadores.

## Proximos passos

1. Repetir multiseed com CICIDS2017 real.
2. Repetir multiseed com UNSW-NB15 real.
3. Adicionar MCC ao agregador.
4. Adicionar testes estatisticos pareados.

