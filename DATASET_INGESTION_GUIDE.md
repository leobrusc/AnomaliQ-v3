# Dataset Ingestion Guide

Data: 2026-06-18

## Estado local observado

Diretorios verificados:

```text
data/raw/cicids2017/ -> ausente
data/raw/unsw_nb15/  -> ausente
```

Como os CSVs reais nao estao presentes, os loaders devem usar fallback sintetico quando `fallback_to_synthetic: true`.

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

## Checklist de ingestao

1. Criar os diretorios `data/raw/cicids2017/` e `data/raw/unsw_nb15/`.
2. Copiar os CSVs reais para os diretorios corretos.
3. Conferir as colunas de rotulo.
4. Executar um benchmark curto com `max_samples_per_class` baixo.
5. Conferir `summary.md` para garantir que nao houve fallback sintetico.
6. Aumentar `max_samples_per_class` progressivamente.
7. Rodar multiseed apenas depois da validacao single-seed.

