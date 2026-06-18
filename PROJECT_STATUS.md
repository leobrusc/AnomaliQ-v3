# PROJECT STATUS - AnomalyQ / AnomaliQ v3

Data: 2026-06-18

## Visao geral

O AnomalyQ v3 e uma suite experimental para deteccao adaptativa de ataques DDoS usando modelos classicos, Quantum Machine Learning e POCs hibridas em ambiente NISQ. O objetivo atual e evoluir da fase POC para TRL 5, validando o pipeline em datasets reais de seguranca como CICIDS2017 e UNSW-NB15.

## Sincronizacao do repositorio

- Branch local atual: `refactor/research-hardening`.
- `origin/master` contem o merge do PR `#1 Refactor/research hardening`.
- Branches relevantes observadas:
  - `origin/feature/experimental-pocs-ddos-qml`;
  - `origin/refactor/research-hardening`;
  - `origin/master`;
  - `master` local antigo em `6ef086b`.
- PR pendente/recente: `#1 Refactor/research hardening`, ja integrado em `origin/master`.
- O repositorio local foi atualizado por fast-forward para o merge commit `790bf86`.

## Arquitetura atual

```text
configs/
legacy/
src/
  data/
  classical/
  quantum/
  evaluation/
  experiments/
results/
  <dataset>/
    <experiment_id>/
      metrics.csv
      summary.md
      config_snapshot.yaml
      experiment_manifest.json
      plots/
      artifacts/
```

## Modulos implementados

- `src/data/synthetic.py`: dataset HTTP sintetico.
- `src/data/cicids_loader.py`: loader binario CICIDS2017.
- `src/data/unsw_loader.py`: loader binario UNSW-NB15.
- `src/data/preprocessing.py`: splits, scaling e PCA para QML.
- `src/classical/baselines.py`: baselines classicos.
- `src/classical/autoencoder.py`: Autoencoder classico via MLPRegressor.
- `src/quantum/qsvm.py`: QSVM com kernel de fidelidade.
- `src/quantum/vqc.py`: VQC com `ZZFeatureMap` e `RealAmplitudes`.
- `src/quantum/vqe_score.py`: score Hamiltoniano com threshold configuravel.
- `src/quantum/qaoa_graph.py`: Max-Cut em grafo pequeno.
- `src/quantum/qae.py`: interface QAE com fallback AE classico.
- `src/quantum/falqon_drift.py`: POC de drift temporal.
- `src/quantum/nisq_noise.py`: benchmark NISQ com Aer/fallback.
- `src/evaluation/reproducibility.py`: manifestos e tracking.
- `src/experiments/run_all.py`: orquestracao completa.
- `src/experiments/run_multiseed.py`: plano executavel para multiplas seeds.

## POCs existentes

- Baselines classicos.
- QSVM-ZZ e QSVM-Pauli.
- VQC com convergencia.
- QAE placeholder baseado em AE classico.
- QAOA Max-Cut em grafo de trafego.
- VQE Hamiltonian Score com threshold.
- FALQON drift placeholder funcional.
- Benchmark NISQ.

## Datasets suportados

- Sintetico HTTP: sempre disponivel.
- CICIDS2017: CSVs esperados em `data/raw/cicids2017/`; fallback sintetico configuravel.
- UNSW-NB15: CSVs esperados em `data/raw/unsw_nb15/`; fallback sintetico configuravel.

## Modelos classicos implementados

- SVM-RBF.
- Random Forest.
- Logistic Regression.
- XGBoost, se disponivel.
- Isolation Forest.
- Autoencoder classico.

## Modelos quanticos implementados

- QSVM-ZZ.
- QSVM-Pauli.
- VQC.
- VQE Hamiltonian Score.
- QAOA Max-Cut POC.
- QAE interface.
- NISQ noise benchmark.

## Resultados sinteticos ja obtidos

Validacao minima executada:

```powershell
python -m compileall src legacy
python -m src.experiments.run_all --config configs/synthetic.yaml --experiment-name resume_validation
```

Resultado: passou.

Diretorio gerado:

```text
results/synthetic/resume_validation-20260618T125111Z/
```

Arquivos verificados:

- `metrics.csv`;
- `summary.md`;
- `experiment_manifest.json`;
- `config_snapshot.yaml`;
- graficos em `plots/`;
- artefatos em `artifacts/`.

Validacao final executada:

```powershell
python -m src.experiments.run_all --config configs/synthetic.yaml --experiment-name final_resume_validation
```

Diretorio gerado:

```text
results/synthetic/final_resume_validation-20260618T125913Z/
```

Resultado: passou. O VQE Hamiltonian Score agora registra threshold supervisionado por validacao (`vqe_threshold_strategy=validation`) e direcao do limiar (`vqe_threshold_direction`).

## CICIDS2017

Suporte atual:

- `src/data/cicids_loader.py`;
- `configs/cicids_ddos.yaml`;
- fallback sintetico quando `data/raw/cicids2017/*.csv` nao existe.

Estado local: nenhum CSV encontrado em `data/raw/cicids2017/`.

Execucao realizada com fallback sintetico:

```powershell
python -m src.experiments.run_all --config configs/cicids_ddos.yaml --experiment-name cicids_initial_benchmark
```

Diretorio:

```text
results/cicids2017/cicids_initial_benchmark-20260618T130033Z/
```

## UNSW-NB15

Suporte atual:

- `src/data/unsw_loader.py`;
- `configs/unsw_nb15.yaml`;
- fallback sintetico quando `data/raw/unsw_nb15/*.csv` nao existe.

Estado local: nenhum CSV encontrado em `data/raw/unsw_nb15/`.

Execucao realizada com fallback sintetico:

```powershell
python -m src.experiments.run_all --config configs/unsw_nb15.yaml --experiment-name unsw_initial_benchmark
```

Diretorio:

```text
results/unsw_nb15/unsw_initial_benchmark-20260618T130033Z/
```

## Limitacoes atuais

- QAE ainda nao e implementacao quantica completa.
- FALQON ainda e placeholder funcional.
- NISQ benchmark ainda precisa executar mais circuitos ruidosos reais, nao apenas pipeline rapido.
- CICIDS2017/UNSW precisam ser validados com arquivos reais.
- Resultados QML usam amostras pequenas por custo de simulacao.
- Notebooks ainda sao legado/compatibilidade.

## Divida tecnica

Ver `TECHNICAL_DEBT.md`.

Principais itens:

- consolidar/remover legado apos migracao completa;
- adicionar lint/test tooling;
- fortalecer loaders reais;
- separar metricas classificatorias e nao classificatorias;
- salvar metadados de ambiente completos.

## Proximos passos para TRL 5

1. Baixar e posicionar CICIDS2017 em `data/raw/cicids2017/`.
2. Baixar e posicionar UNSW-NB15 em `data/raw/unsw_nb15/`.
3. Rodar benchmarks reais sem fallback.
4. Executar `run_multiseed.py` com seeds `42`, `123`, `2026`.
5. Calcular media/desvio padrao e testes Wilcoxon/Friedman.
6. Melhorar QAE e benchmark NISQ circuito-real.
7. Produzir tabelas e graficos para publicacao.
