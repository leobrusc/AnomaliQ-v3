# Research Roadmap 2026

Data: 2026-06-18

## Fase A - CICIDS2017 real

Objetivo:
- Executar benchmark real BENIGN vs DDoS com CICIDS2017.

Tarefas:
- Adicionar CSVs em `data/raw/cicids2017/`.
- Validar loader sem fallback sintetico.
- Rodar single-seed.
- Rodar multiseed.
- Comparar SVM-RBF, Random Forest, Logistic Regression, Isolation Forest, QSVM-ZZ, QSVM-Pauli, VQC e VQE Score.

Saida:
- Tabelas por seed.
- Agregado media/desvio padrao.
- Graficos principais.

## Fase B - UNSW-NB15 real

Objetivo:
- Validar generalizacao em dataset real secundario.

Tarefas:
- Adicionar CSVs em `data/raw/unsw_nb15/`.
- Validar normal vs attack.
- Revisar tratamento de categoricas.
- Rodar single-seed e multiseed.

Saida:
- Comparacao cross-dataset.
- Discussao sobre diferencas de distribuicao.

## Fase C - Multiseed

Objetivo:
- Medir estabilidade experimental.

Seeds:

```text
42, 123, 2026
```

Tarefas:
- Agregar F1, ROC-AUC e MCC.
- Gerar barras de erro.
- Separar modelos comparaveis e POCs.

## Fase D - Analise estatistica

Objetivo:
- Verificar significancia das diferencas entre modelos.

Testes:
- Wilcoxon para comparacoes pareadas.
- Friedman para multiplos modelos.
- Pos-hoc Nemenyi se houver amostras suficientes.

Cuidados:
- Nao misturar POCs sem predicao supervisionada com classificadores completos.
- Reportar tamanho de efeito quando possivel.

## Fase E - Artigo

Objetivo:
- Consolidar contribuicoes cientificas do AnomalyQ.

Estrutura sugerida:
- Introducao e motivacao.
- Trabalhos relacionados.
- Metodologia.
- Dataset e protocolo experimental.
- Modelos classicos e quanticos.
- Resultados.
- Discussao NISQ.
- Ameacas a validade.
- Conclusao.

Contribuicoes:
- Suite reprodutivel para DDoS adaptativo.
- Comparacao classica vs QML em datasets reais.
- Analise de custo NISQ.
- Discussao de limites praticos em ambiente NISQ.

## Fase F - IBM Quantum

Objetivo:
- Migrar POCs selecionadas para backend quantum real ou runtime IBM Quantum.

Pre-requisitos:
- Reduzir circuitos para poucos qubits.
- Controlar profundidade e CNOTs.
- Selecionar subconjuntos pequenos.
- Definir budget de shots.
- Registrar backend, queue time, noise model e transpilation settings.

Experimentos candidatos:
- QSVM com poucos samples.
- VQC com baixa profundidade.
- VQE Score em circuito pequeno.

Saida:
- Comparacao simulador ideal vs ruidoso vs hardware real.
- Discussao de degradacao e mitigacao de erro.

