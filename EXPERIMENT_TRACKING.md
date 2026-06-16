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
