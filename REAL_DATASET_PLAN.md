# Plano de datasets reais para TRL 5

Objetivo: preparar o AnomaliQ v3 para validacao em datasets reais de seguranca, com foco inicial em CICIDS2017 e UNSW-NB15.

## Estado local dos dados

No momento da retomada, `data/raw/` existe, mas nao contem arquivos CSV. Portanto:

- CICIDS2017 real nao foi executado; `configs/cicids_ddos.yaml` usa fallback sintetico quando `fallback_to_synthetic: true`.
- UNSW-NB15 real nao foi executado; `configs/unsw_nb15.yaml` usa fallback sintetico quando `fallback_to_synthetic: true`.

## CICIDS2017

Local esperado:

```text
data/raw/cicids2017/*.csv
```

Config:

```text
configs/cicids_ddos.yaml
```

Requisitos do loader:

- procurar CSVs em `data/raw/cicids2017/`;
- padronizar nomes de colunas;
- localizar coluna de rotulo configurada;
- filtrar `BENIGN` vs `DDoS`;
- remover NaN e infinitos;
- converter features para numerico;
- limitar amostras por classe;
- salvar processado em `data/processed/cicids2017_ddos_binary_processed.csv`;
- manter fallback sintetico configuravel.

Comando:

```powershell
python -m src.experiments.run_all --config configs/cicids_ddos.yaml --experiment-name cicids_initial_benchmark
```

## UNSW-NB15

Local esperado:

```text
data/raw/unsw_nb15/*.csv
```

Config:

```text
configs/unsw_nb15.yaml
```

Requisitos do loader:

- procurar CSVs em `data/raw/unsw_nb15/`;
- aceitar coluna binaria `label` ou coluna `attack_cat`;
- converter `normal` para classe 0 e ataque para classe 1;
- codificar colunas categoricas via fatorizacao simples;
- mapear features UNSW para o contrato comum de features;
- limitar amostras por classe;
- salvar processado em `data/processed/unsw_nb15_binary_processed.csv`;
- manter fallback sintetico configuravel.

Comando:

```powershell
python -m src.experiments.run_all --config configs/unsw_nb15.yaml --experiment-name unsw_initial_benchmark
```

## Protocolo de comparacao

Modelos classicos:

- SVM-RBF;
- Random Forest;
- Logistic Regression;
- XGBoost, se instalado;
- Isolation Forest.

Modelos quanticos:

- QSVM-ZZ;
- QSVM-Pauli;
- VQC;
- VQE Hamiltonian Score com threshold configurado.

## Multiplas seeds

Seeds propostas:

```text
42, 123, 2026
```

Comando:

```powershell
python -m src.experiments.run_multiseed --config configs/cicids_ddos.yaml --experiment-name cicids_multiseed --seeds 42 123 2026
```

Estatistica sugerida:

- media e desvio padrao por modelo;
- Wilcoxon para comparacao pareada de dois modelos;
- Friedman para comparacao de multiplos modelos.

## Criterios para TRL 5

- Rodar pelo menos CICIDS2017 e UNSW-NB15 reais sem fallback.
- Registrar manifestos, configs e hashes Git para todas as execucoes.
- Separar resultados por dataset e seed.
- Reportar limitacoes dos modelos quanticos sob custo de simulacao.
- Incluir analise estatistica minima entre modelos classicos e quanticos.
