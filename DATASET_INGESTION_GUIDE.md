# Dataset Ingestion Guide

Data: 2026-06-18

## Estado local observado

Diretorios verificados:

```text
data/raw/cicids2017/ -> ausente
data/raw/unsw_nb15/  -> ausente
```

Como os CSVs reais nao estao presentes, os loaders devem usar fallback sintetico quando `fallback_to_synthetic: true` e `require_real_dataset: false`.

Para benchmark real publicavel, use os configs strict. Nesse modo, a execucao falha de forma controlada se os CSVs reais nao existirem.

## Estrutura esperada

```text
data/
  raw/
    cicids2017/
      *.csv
    unsw_nb15/
      *.csv
  processed/
```

`data/raw/` e ignorado pelo Git. Os datasets reais nao devem ser versionados.

## CICIDS2017

Config principal:

```yaml
dataset:
  mode: cicids2017
  cicids:
    raw_dir: data/raw/cicids2017
    processed_dir: data/processed
    label_column: Label
    target_labels: [BENIGN, DDoS]
    max_samples_per_class: 1000
    require_real_dataset: false
    fallback_to_synthetic: true
```

Arquivos esperados:

```text
data/raw/cicids2017/*.csv
```

Requisitos:

- Os CSVs devem conter uma coluna de rotulo, por padrao `Label`.
- O modo binario usa `BENIGN` como classe 0 e `DDoS` como classe 1.
- Labels adicionais sao filtrados fora do benchmark DDoS binario.
- Colunas nao numericas ou problemáticas devem ser removidas ou convertidas pelo loader.
- Valores NaN e infinitos sao tratados antes do preprocessamento.
- O loader salva uma versao processada em `data/processed/`.

Comando de validacao:

```powershell
python -m src.experiments.run_all --config configs/cicids_ddos.yaml --experiment-name cicids_real_benchmark
```

Modo benchmark real strict:

```yaml
dataset:
  mode: cicids2017
  cicids:
    raw_dir: data/raw/cicids2017
    require_real_dataset: true
    fallback_to_synthetic: false
```

Comando strict:

```powershell
python -m src.experiments.run_all --config configs/cicids_ddos_real_strict.yaml --experiment-name cicids_real_benchmark
```

Se os CSVs nao existirem, a mensagem esperada e:

```text
CICIDS2017 dataset not found.
Expected CSV files under:
data/raw/cicids2017/*.csv
```

## UNSW-NB15

Config principal:

```yaml
dataset:
  mode: unsw_nb15
  unsw:
    raw_dir: data/raw/unsw_nb15
    processed_dir: data/processed
    label_column: label
    normal_labels: [0, Normal, NORMAL]
    attack_labels: [1]
    max_samples_per_class: 1000
    require_real_dataset: false
    fallback_to_synthetic: true
```

Arquivos esperados:

```text
data/raw/unsw_nb15/*.csv
```

Requisitos:

- Preferir CSVs oficiais com coluna `label`.
- Se `label` nao existir, revisar o loader para usar `attack_cat` de forma explicita.
- Colunas categoricas sao codificadas para uso no pipeline comum.
- O modo binario usa normal vs attack.
- O loader salva uma versao processada em `data/processed/`.

Comando de validacao:

```powershell
python -m src.experiments.run_all --config configs/unsw_nb15.yaml --experiment-name unsw_real_benchmark
```

Modo benchmark real strict:

```yaml
dataset:
  mode: unsw_nb15
  unsw:
    raw_dir: data/raw/unsw_nb15
    require_real_dataset: true
    fallback_to_synthetic: false
```

Comando strict:

```powershell
python -m src.experiments.run_all --config configs/unsw_nb15_real_strict.yaml --experiment-name unsw_real_benchmark
```

Se os CSVs nao existirem, a mensagem esperada e:

```text
UNSW-NB15 dataset not found.
Expected CSV files under:
data/raw/unsw_nb15/*.csv
```

## Modos de execucao

### Desenvolvimento com fallback

Use:

```powershell
python -m src.experiments.run_all --config configs/cicids_ddos.yaml --experiment-name cicids_fallback_check
python -m src.experiments.run_all --config configs/unsw_nb15.yaml --experiment-name unsw_fallback_check
```

Esses configs mantem:

```yaml
require_real_dataset: false
fallback_to_synthetic: true
```

### Benchmark real strict

Use:

```powershell
python -m src.experiments.run_all --config configs/cicids_ddos_real_strict.yaml --experiment-name cicids_real_benchmark
python -m src.experiments.run_all --config configs/unsw_nb15_real_strict.yaml --experiment-name unsw_real_benchmark
```

Esses configs mantem:

```yaml
require_real_dataset: true
fallback_to_synthetic: false
```

Eles devem ser usados para resultados publicaveis, pois impedem que uma execucao sem CSV real produza resultados sinteticos por engano.

## Checklist de ingestao

1. Criar os diretorios `data/raw/cicids2017/` e `data/raw/unsw_nb15/`.
2. Copiar os CSVs reais para os diretorios corretos.
3. Conferir as colunas de rotulo.
4. Executar um benchmark curto com config normal para validar pipeline.
5. Executar o config strict para garantir que nao houve fallback sintetico.
6. Conferir `summary.md` e `experiment_manifest.json`.
7. Aumentar `max_samples_per_class` progressivamente.
8. Rodar multiseed apenas depois da validacao single-seed.
