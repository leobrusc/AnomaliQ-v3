# Roadmap AnomaliQ v4

Objetivo do v4: transformar a suite POC do AnomaliQ v3 em uma plataforma experimental robusta para publicacao cientifica sobre deteccao adaptativa de DDoS com QML em ambientes NISQ.

## Fase 1 - Higiene de engenharia

Meta: estabilizar a base antes de expandir experimentos.

- Remover ou deprecar modulos legados em `src/`.
- Atualizar `notebooks/experiment_01.ipynb` para a nova arquitetura.
- Adicionar `pyproject.toml` com `ruff`, formato, regras de lint e configuracao de pytest.
- Criar `requirements-dev.txt`.
- Criar testes smoke:
  - `run_baselines` gera pelo menos SVM-RBF e Random Forest.
  - `run_qsvm` gera QSVM-ZZ ou registra falha clara.
  - `run_vqc` gera `vqc_convergence.png`.
  - `run_all` gera `metrics.csv` e `summary.md`.
- Adicionar CI GitHub Actions para Windows e Linux.

Entregavel: repositorio importavel, lintavel e testavel.

## Fase 2 - Dataset real CICIDS2017

Meta: tornar resultados empiricos defensaveis.

- Implementar normalizacao robusta de colunas CICIDS2017.
- Criar manifesto de arquivos aceitos: dia, tipo de ataque, labels esperadas.
- Criar pipeline `data/processed/cicids_ddos_binary.parquet`.
- Adicionar split temporal e split estratificado.
- Registrar hash dos CSVs de origem.
- Implementar relatorio de qualidade dos dados:
  - linhas totais;
  - taxa de labels descartados;
  - nulos/infinito;
  - distribuicao de classes;
  - features faltantes.

Entregavel: `configs/cicids_ddos.yaml` executa com dataset real sem fallback silencioso quando `strict=true`.

## Fase 3 - QAE real

Meta: substituir o placeholder por experimento quântico minimo.

- Definir arquitetura encoder-latent-trash-decoder.
- Treinar somente com benignos.
- Usar loss de fidelidade/projecao nos qubits trash.
- Calibrar threshold em validacao benigna.
- Comparar:
  - AE classico;
  - QAE statevector;
  - QAE ruidoso com Aer.
- Registrar profundidade, CNOTs, parametros e tempo.

Entregavel: `run_qae.py` produz linha QAE real e linha AE classico comparativa.

## Fase 4 - Benchmark NISQ circuito-real

Meta: medir ruido no objeto quântico correto.

- Executar circuitos em `AerSimulator` com `NoiseModel`.
- Adicionar modelos de ruido:
  - depolarizing;
  - thermal relaxation;
  - readout error;
  - combinacoes calibradas.
- Rodar multiplas seeds e shots.
- Medir degradacao por:
  - numero de qubits;
  - profundidade;
  - CNOT count;
  - reps do feature map;
  - optimizer budget.
- Salvar `results/artifacts/environment.json`.

Entregavel: tabela NISQ com intervalos de confianca e curvas por ruido.

## Fase 5 - VQE Hamiltoniano calibrado

Meta: tornar o score Hamiltoniano informativo.

- Aprender pesos `w_i` e `J_ij` por otimizacao classica supervisionada.
- Comparar Hamiltonianos:
  - diagonal Z;
  - ZZ pairwise;
  - Ising com bias;
  - Hamiltoniano por mutual information.
- Calibrar threshold em validacao.
- Reportar curvas ROC/PR do score.

Entregavel: VQE score com F1 acima de baseline aleatorio e interpretabilidade dos termos.

## Fase 6 - FALQON/adaptacao temporal

Meta: ir alem de placeholder por retreino.

- Formalizar janelas temporais com drift gradual e abrupto.
- Medir pre-drift, queda, tempo de recuperacao e pos-drift.
- Implementar controle inspirado em FALQON para atualizacao de parametros variacionais.
- Comparar contra:
  - retreino periodico;
  - online logistic regression;
  - drift detectors classicos.

Entregavel: experimento temporal com curva F1 e metricas de recuperacao.

## Fase 7 - Publicacao cientifica

Meta: gerar pacote reprodutivel para paper.

- Definir hipoteses:
  - H1: QML melhora robustez sob baixa dimensionalidade?
  - H2: ruido NISQ degrada F1 proporcionalmente a profundidade/CNOTs?
  - H3: abordagem hibrida melhora recuperacao sob drift?
- Rodar todas as configuracoes com multiplas seeds.
- Adicionar baseline classico forte:
  - Gradient Boosting;
  - calibrated SVM;
  - Isolation Forest tuned;
  - AE classico tuned.
- Reportar media, desvio padrao e intervalos de confianca.
- Preparar artefatos:
  - tabela LaTeX;
  - figuras finais;
  - appendix de configs;
  - DOI/dataset instructions.

Entregavel: `paper/` ou `reports/paper_artifacts/` com tabelas e figuras reproduziveis.

## Indicadores de prontidao v4

- `python -m pytest` passa.
- `python -m ruff check .` passa.
- `python -m src.experiments.run_all --config configs/synthetic.yaml` passa em menos de 3 minutos.
- `python -m src.experiments.run_all --config configs/cicids_ddos.yaml` passa com CICIDS2017 real.
- `results/summary.md` inclui ambiente, hash Git, configs e limitacoes.
- QAE, QAOA, VQE e NISQ deixam claro quando sao quantum real, simulacao ideal, simulacao ruidosa ou fallback classico.
