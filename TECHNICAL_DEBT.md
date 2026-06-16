# Divida tecnica AnomaliQ v3

Este documento lista a divida tecnica identificada na revisao pre-merge. Nenhum item abaixo foi corrigido nesta etapa; o objetivo e orientar priorizacao.

## Prioridade alta

| ID | Area | Evidencia | Risco | Acao recomendada |
| --- | --- | --- | --- | --- |
| TD-001 | Modulos legados quebrados | `src/qaoa_cluster.py` falha ao importar `Sampler`; `src/vqe_score.py` falha ao importar `Estimator` | Importacao global ou uso por notebook pode quebrar usuarios | Remover, migrar para `src/quantum/*` ou marcar como deprecated com wrappers compativeis |
| TD-002 | Notebook desatualizado | `notebooks/experiment_01.ipynb` importa `preprocessing`, `feature_map`, `qsvm`, `vqc`, `alerts` | Tutorial executa caminho antigo e possivelmente quebrado | Atualizar notebook para `python -m src.experiments.*` ou novos pacotes |
| TD-003 | Tooling ausente | `ruff`, `flake8` e `pytest` nao instalados | Nao ha garantia automatizada de estilo, imports e regressao | Adicionar `requirements-dev.txt` ou `pyproject.toml` com ruff/pytest |
| TD-004 | Benchmark NISQ parcialmente aproximado | `benchmark_noise` cria `NoiseModel`, mas mede F1 com perturbacao de features | Resultado pode ser interpretado como simulacao ruidosa de circuito sem ser | Implementar execucao Aer real por circuito/modelo |
| TD-005 | QAE placeholder | `src/quantum/qae.py` chama Autoencoder classico e renomeia o modelo | POC nao valida reivindicacao de QAE | Implementar QAE variacional ou explicitar como baseline classico |

## Prioridade media

| ID | Area | Evidencia | Risco | Acao recomendada |
| --- | --- | --- | --- | --- |
| TD-006 | Duplicacao de codigo | Modulos soltos em `src/` duplicam pacotes novos | Manutencao dupla e inconsistencias de API | Consolidar em pacotes e remover camada antiga |
| TD-007 | CICIDS2017 fraco | Colunas ausentes recebem zero; mapeamento parcial | Resultados em dataset real podem ser enviesados | Criar schema robusto, normalizacao de nomes e feature engineering real |
| TD-008 | Resultados misturados | `metrics.csv` mistura classificadores e POCs nao classificatorias | Analise automatica fica fragil e cheia de `NaN` | Separar `classification_metrics.csv`, `quantum_metrics.csv`, `artifacts_index.csv` |
| TD-009 | Politica de results | `results/` versionado e sobrescrito por `run_all.py` | Diffs ruidosos e perda de historico local | Usar `results/reference/` versionado e `results/runs/` ignorado |
| TD-010 | Calibracao VQE | Ultima execucao registrou F1 `0.0` para VQE | Hamiltoniano/threshold nao sustentam conclusao experimental | Aprender pesos `w_i`, `J_ij` ou calibrar score em validacao |
| TD-011 | QSVM instavel | QSVM em amostra pequena teve F1 baixo e alta variancia esperada | Comparacao cientifica pode ser injusta | Rodar multiplas seeds e tamanhos de amostra |
| TD-012 | Logging/falhas | Muitos `except Exception` amplos | Falhas reais podem virar fallback silencioso | Registrar stack trace completo em `failures.csv` e separar dependencia ausente de bug |

## Prioridade baixa

| ID | Area | Evidencia | Risco | Acao recomendada |
| --- | --- | --- | --- | --- |
| TD-013 | Imports nao usados | `numpy` em `src/preprocessing.py`; `numpy`, `VQE`, `COBYLA` em `src/vqe_score.py` | Ruido de manutencao | Resolver junto da remocao dos legados |
| TD-014 | Docstrings | Funcoes publicas novas quase sem docstrings | Onboarding mais lento | Adicionar docstrings curtos com inputs/outputs |
| TD-015 | Metadata experimental | `summary.md` nao inclui versoes, hash Git, ambiente | Reprodutibilidade incompleta | Salvar `environment.json` por execucao |
| TD-016 | Config schema | YAML sem validacao | Erros de configuracao podem falhar tarde | Usar dataclasses/Pydantic leve ou validacao manual |
| TD-017 | Alert metrics | `estimated_time_to_detection` usa indice de amostra como tempo | Interpretacao operacional limitada | Usar timestamps/janelas reais para TTD |

## Decisao sugerida para merge

Merge como POC experimental: aceitavel.

Merge como base estavel: bloquear ate resolver TD-001, TD-002, TD-003 e documentar TD-004/TD-005 explicitamente no README.

## Checklist recomendado

- [ ] Atualizar notebook para a nova API.
- [ ] Remover ou deprecar modulos legados quebrados.
- [ ] Adicionar `ruff` e `pytest`.
- [ ] Criar testes smoke para `run_baselines`, `run_qsvm`, `run_vqc` e `run_all`.
- [ ] Separar resultados de referencia de resultados locais.
- [ ] Melhorar loader CICIDS2017.
- [ ] Implementar benchmark NISQ com Aer real.
- [ ] Implementar QAE variacional ou renomear POC para AE baseline.
