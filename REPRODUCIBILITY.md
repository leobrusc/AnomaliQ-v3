# Reprodutibilidade

O AnomaliQ v3 usa uma camada explicita de tracking para preservar o contexto de cada execucao experimental. O objetivo e impedir que uma nova rodada sobrescreva resultados anteriores e permitir auditoria de configuracao, codigo e backend.

## Como executar

```powershell
python -m src.experiments.run_all --config configs/synthetic.yaml --experiment-name synthetic-smoke
```

O argumento `--experiment-name` e opcional. Quando informado, ele vira o prefixo do identificador da execucao. O sufixo e sempre um timestamp UTC, portanto execucoes repetidas criam diretorios distintos.

## Estrutura gerada

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

## Arquivos de reprodutibilidade

### config_snapshot.yaml

Copia integral da configuracao YAML carregada no inicio da execucao. Esse arquivo deve ser usado para reexecutar uma rodada historica mesmo que `configs/synthetic.yaml` ou `configs/cicids_ddos.yaml` mudem no futuro.

### experiment_manifest.json

Manifesto JSON com:

- `experiment_id`
- `git_commit_hash`
- `dataset`
- `seed`
- `n_qubits`
- `feature_map`
- `optimizer`
- `timestamp`
- `backend`
- `output_dir`
- `config_path`

## Seeds e determinismo

A configuracao central usa `seed: 42`. Os modelos classicos e selecao de amostras quanticas recebem essa seed quando a biblioteca permite. Algoritmos variacionais e simuladores podem ainda ter pequenas variacoes dependendo de versao de Qiskit, primitivas e backend.

Para rodadas com multiplas seeds:

```powershell
python -m src.experiments.run_multiseed --config configs/cicids_ddos.yaml --experiment-name cicids_multiseed --seeds 42 123 2026
```

O script salva `multiseed_all_metrics.csv` e `multiseed_summary.csv` no diretorio agregado. A interpretacao recomendada e reportar media, desvio padrao e teste estatistico pareado quando houver a mesma particao/seeds por modelo.

## Datasets reais

Coloque os arquivos locais em:

```text
data/raw/cicids2017/*.csv
data/raw/unsw_nb15/*.csv
```

Os loaders salvam os dados tratados em `data/processed/`. Quando `fallback_to_synthetic: true`, ausencia de CSVs reais nao quebra a execucao; o aviso fica em `summary.md`.

## Limites atuais

- O manifesto registra o commit e backend detectado, mas ainda nao salva versoes detalhadas de todas as dependencias.
- O benchmark NISQ usa Aer quando disponivel, mas a degradacao agregada ainda e medida no pipeline rapido atual.
- `results/` contem tambem resultados historicos da fase anterior na raiz; novos runners escrevem em `results/<dataset>/<experiment_id>/`.
- QAE e FALQON ainda sao POCs, nao implementacoes cientificas finais.

## Recomendacao para publicacao

Para resultados publicaveis, manter junto de cada tabela:

- `config_snapshot.yaml`;
- `experiment_manifest.json`;
- hash Git;
- versoes de dependencias;
- seed;
- dataset real usado e hash dos CSVs originais.
