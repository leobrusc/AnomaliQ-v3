# Experiment Tracking

Este documento descreve a organizacao de resultados do AnomaliQ v3 apos a consolidacao pre-CICIDS2017.

## Convencao de diretorios

Toda execucao nova escreve em:

```text
results/<dataset>/<experiment_id>/
```

Exemplo:

```text
results/synthetic/run-20260616T120000Z/
results/synthetic/synthetic-smoke-20260616T120500Z/
results/cicids2017/cicids-ddos-baseline-20260616T121000Z/
```

## Conteudo de cada execucao

```text
metrics.csv
summary.md
config_snapshot.yaml
experiment_manifest.json
plots/
artifacts/
```

`failures.csv` e criado apenas quando algum experimento falha e o runner consegue continuar.

## Runners suportados

Todos os runners aceitam `--experiment-name`:

```powershell
python -m src.experiments.run_all --config configs/synthetic.yaml --experiment-name full-suite
python -m src.experiments.run_baselines --config configs/synthetic.yaml --experiment-name baselines
python -m src.experiments.run_qsvm --config configs/synthetic.yaml --experiment-name qsvm
python -m src.experiments.run_vqc --config configs/synthetic.yaml --experiment-name vqc
python -m src.experiments.run_vqe --config configs/synthetic.yaml --experiment-name vqe
python -m src.experiments.run_qaoa --config configs/synthetic.yaml --experiment-name qaoa
python -m src.experiments.run_falqon --config configs/synthetic.yaml --experiment-name falqon
python -m src.experiments.run_multiseed --config configs/synthetic.yaml --experiment-name multiseed --seeds 42 123 2026
```

Datasets reais:

```powershell
python -m src.experiments.run_all --config configs/cicids_ddos.yaml --experiment-name cicids_initial_benchmark
python -m src.experiments.run_all --config configs/unsw_nb15.yaml --experiment-name unsw_initial_benchmark
```

## Manifesto

O manifesto e produzido por `src/evaluation/reproducibility.py` e tem a seguinte finalidade:

- associar resultados ao commit;
- indicar dataset e seed;
- registrar configuracao quantica basica;
- registrar timestamp UTC;
- apontar backend disponivel.

## Politica de sobrescrita

O ID inclui timestamp UTC, entao uma execucao nova nao sobrescreve a anterior. O argumento `--reset` continua disponivel para limpar arquivos dentro do diretorio da execucao corrente, mas como o diretorio e novo por padrao, ele raramente e necessario.

## Relacao com resultados antigos

Resultados antigos ainda podem existir diretamente em `results/`. Eles foram mantidos para preservar o historico da fase POC. A partir desta consolidacao, resultados novos devem ser avaliados nos subdiretorios por dataset.

## Interpretacao de resultados

- `metrics.csv` e a tabela principal para comparacao de classificadores.
- `summary.md` registra avisos, fallbacks e limitacoes da execucao.
- `config_snapshot.yaml` deve ser usado para reproduzir uma execucao especifica.
- `experiment_manifest.json` conecta resultado, commit e backend.
- `artifacts/` contem particionamentos, curvas intermediarias e resultados auxiliares.
- `plots/` contem figuras geradas automaticamente.
