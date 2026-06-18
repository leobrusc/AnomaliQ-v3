# TRL5 Readiness Report

Data: 2026-06-18

## Objetivo

Avaliar a prontidao do AnomalyQ para sair da validacao sintetica e entrar em benchmark real com datasets de seguranca, especialmente CICIDS2017 e UNSW-NB15, mantendo reproducibilidade, rastreabilidade e comparacao entre modelos classicos, QML e POCs hibridas/NISQ.

## Maturidade atual

Nivel estimado: pre-TRL5.

O projeto ja possui uma pipeline experimental modular, configuracoes YAML, loaders preparados para datasets reais, fallback sintetico, tracking por execucao e geracao automatica de metricas e graficos. A validacao sintetica funciona e a execucao multiseed foi validada.

Para TRL5 completo, ainda falta executar com dados reais locais, congelar protocolo estatistico, registrar versoes de ambiente e produzir resultados agregados com intervalos de confianca ou testes pareados.

## Funcionalidades implementadas

- Dataset sintetico HTTP binario para BENIGN vs DDoS.
- Loader CICIDS2017 com fallback sintetico.
- Loader UNSW-NB15 com fallback sintetico.
- Preprocessamento comum com normalizacao, split e reducao via PCA para QML.
- Experiment tracking em `results/<dataset>/<experiment_id>/`.
- `experiment_manifest.json`, `config_snapshot.yaml`, `metrics.csv` e `summary.md`.
- Baselines classicos:
  - Logistic Regression;
  - Random Forest;
  - SVM-RBF;
  - Isolation Forest;
  - Autoencoder classico quando dependencias permitem.
- Modelos/POCs quanticos:
  - QSVM-ZZ;
  - QSVM-Pauli;
  - VQC;
  - VQE Hamiltonian Score com threshold;
  - QAE interface com fallback classico;
  - QAOA MaxCut POC;
  - FALQON Drift POC;
  - benchmark NISQ em simulacao.
- Execucao multiseed via `src/experiments/run_multiseed.py`.

## Limitacoes atuais

- CICIDS2017 e UNSW-NB15 ainda precisam estar fisicamente em `data/raw/`.
- Os resultados reais ainda nao foram produzidos; execucoes anteriores com esses configs usaram fallback sintetico.
- QSVM e VQC usam subconjuntos reduzidos por custo computacional.
- QAE ainda e interface/fallback classico, nao um autoencoder quantico completo.
- QAOA e FALQON sao POCs estruturais, nao classificadores supervisionados completos.
- VQE gera score continuo; comparacao por F1 depende de threshold configurado.
- MCC ainda deve ser adicionado a `src/evaluation/metrics.py` para o protocolo publicavel.
- Resultados antigos em `results/synthetic/run-*` existem no historico da `master`; novas execucoes completas devem ficar fora do Git.

## Requisitos para benchmark real

1. Baixar e posicionar CICIDS2017 em `data/raw/cicids2017/*.csv`.
2. Baixar e posicionar UNSW-NB15 em `data/raw/unsw_nb15/*.csv`.
3. Confirmar nomes de colunas e labels reais.
4. Executar validacao single-seed para cada dataset.
5. Executar multiseed com seeds `42`, `123` e `2026`.
6. Registrar ambiente Python, versoes de Qiskit, scikit-learn, pandas, numpy e dependencias opcionais.
7. Exportar tabelas agregadas por modelo, dataset e seed.
8. Executar analise estatistica pareada.

## Requisitos para publicacao cientifica

- Protocolo experimental congelado antes de rodar benchmarks finais.
- Separacao clara entre classificadores comparaveis por F1 e POCs sem predicao supervisionada direta.
- Relatorio de ameacas a validade:
  - viés de amostragem;
  - reducao PCA para poucos qubits;
  - simulacao NISQ simplificada;
  - datasets de IDS com artefatos conhecidos;
  - custo de treinamento QML em simulador classico.
- Tabelas com media, desvio padrao e ranking por dataset.
- Testes estatisticos:
  - Wilcoxon para comparacoes pareadas;
  - Friedman/Nemenyi para multiplos modelos.
- Reprodutibilidade:
  - commit hash;
  - configs;
  - seeds;
  - manifestos;
  - logs de falhas;
  - versoes de dependencias.

## Readiness gate

O AnomalyQ esta pronto para iniciar a fase de benchmark real controlado, desde que os CSVs reais sejam adicionados localmente e o protocolo de metricas seja fechado antes da execucao final.

