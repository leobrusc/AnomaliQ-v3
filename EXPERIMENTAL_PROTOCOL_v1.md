# Experimental Protocol v1

Data: 2026-06-18

## Hipotese cientifica

Modelos de Quantum Machine Learning e hibridos NISQ podem capturar estruturas de anomalia em trafego DDoS com desempenho competitivo em relacao a baselines classicos, especialmente quando avaliados em representacoes reduzidas e sob metricas que incluem custo de circuito, robustez a ruido e estabilidade temporal.

## Datasets

- Sintetico HTTP: usado para validacao funcional e reproducibilidade.
- CICIDS2017: benchmark real primario para BENIGN vs DDoS.
- UNSW-NB15: benchmark real secundario para normal vs attack.

## Variaveis independentes

- Dataset: sintetico, CICIDS2017, UNSW-NB15.
- Modelo: Logistic Regression, Random Forest, SVM-RBF, Isolation Forest, QSVM-ZZ, QSVM-Pauli, VQC, VQE Score, FALQON.
- Feature map: ZZFeatureMap, PauliFeatureMap.
- Numero de qubits: valor configurado em YAML.
- Seed: 42, 123, 2026.
- Nivel de ruido NISQ: valores em `experiments.noise_levels`.
- Estrategia de threshold para scores continuos: validation ou percentile.

## Variaveis dependentes

- Desempenho de classificacao.
- Qualidade de alertas.
- Custo computacional.
- Metricas de circuito quantico.
- Degradacao sob ruido.
- Estabilidade entre seeds.

## Metricas de classificacao

- Accuracy.
- Precision.
- Recall.
- F1.
- ROC-AUC.
- MCC.

Observacao: MCC deve ser implementado em `src/evaluation/metrics.py` antes da execucao final publicavel.

## Metricas de mitigacao

- Number of alerts.
- True alerts.
- False alerts.
- Alert precision.
- Estimated time to detection.
- Mitigation delay simulated.

## Metricas NISQ

- Numero de qubits.
- Profundidade do circuito.
- Numero de parametros.
- Numero de CNOTs.
- Tempo de treino.
- Tempo de inferencia.
- Iteracoes do otimizador.
- Loss final.
- Degradacao de F1 sob ruido.

## Procedimento experimental

1. Congelar config YAML por dataset.
2. Validar ingestao real sem fallback sintetico.
3. Executar single-seed para detectar falhas de loader, memoria e tempo.
4. Executar multiseed com seeds `42`, `123`, `2026`.
5. Agregar media e desvio padrao por modelo.
6. Separar classificadores supervisionados de POCs nao diretamente comparaveis.
7. Rodar testes estatisticos.
8. Gerar tabelas e graficos finais.

## Criterios de comparabilidade

- Modelos classicos usam o mesmo split e features normalizadas.
- QSVM e VQC usam a mesma representacao PCA reduzida para qubits.
- VQE Score entra em metricas supervisionadas apenas quando threshold converte score continuo em rotulo.
- QAOA e FALQON devem ser reportados como POCs quando nao produzirem predicao por amostra.

## Saidas esperadas

Cada execucao deve gerar:

```text
metrics.csv
summary.md
config_snapshot.yaml
experiment_manifest.json
plots/
artifacts/
```

Execucoes multiseed devem gerar:

```text
multiseed_all_metrics.csv
multiseed_summary.csv
```

