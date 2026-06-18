# Visualization Roadmap

Data: 2026-06-18

## Graficos atuais

O projeto ja gera:

- Comparacao F1 por modelo.
- Comparacao ROC-AUC por modelo.
- Matriz de confusao do melhor classificador com matriz valida.
- Curva de convergencia VQC.
- Degradacao NISQ por ruido.
- Drift temporal FALQON.

## Limitacoes atuais

- Graficos agregados multiseed ainda nao incluem barras de erro.
- Modelos classificadores e POCs aparecem juntos em alguns relatorios, o que pode confundir interpretacao.
- Nao ha visualizacao consolidada de custo vs desempenho.
- Nao ha grafico dedicado de tempo de execucao.
- Nao ha comparacao direta entre profundidade de circuito, CNOTs e F1.

## Novos graficos propostos

### Radar chart

Objetivo:
- Comparar modelos por F1, ROC-AUC, estabilidade, custo e robustez a ruido.

Uso:
- Apresentacao executiva e comparacao visual rapida.

### Ranking consolidado

Objetivo:
- Ordenar modelos por score composto.

Score sugerido:

```text
score = 0.35 * F1 + 0.25 * ROC-AUC + 0.20 * estabilidade + 0.10 * robustez_ruido + 0.10 * eficiencia
```

Observacao:
- POCs sem predicao supervisionada devem ficar fora do ranking principal.

### Tempo de execucao

Objetivo:
- Mostrar custo de treino e inferencia por modelo.

Eixos:
- Modelo.
- Tempo de treino.
- Tempo de inferencia.

### Profundidade de circuito

Objetivo:
- Comparar custo NISQ entre QSVM, VQC, VQE e QAOA.

Metricas:
- Profundidade.
- Numero de CNOTs.
- Numero de parametros.
- Numero de qubits.

### F1 vs profundidade

Objetivo:
- Avaliar trade-off desempenho/custo quantico.

Eixos:
- X: profundidade do circuito.
- Y: F1.
- Cor: tipo de modelo.
- Tamanho: numero de CNOTs.

### Curvas multiseed com erro

Objetivo:
- Mostrar media e desvio padrao por modelo e dataset.

Graficos:
- F1 medio com barras de erro.
- ROC-AUC medio com barras de erro.
- MCC medio com barras de erro.

## Prioridade

1. Barras de erro multiseed.
2. Tempo de execucao.
3. Profundidade/CNOTs.
4. F1 vs profundidade.
5. Ranking consolidado.
6. Radar chart.

