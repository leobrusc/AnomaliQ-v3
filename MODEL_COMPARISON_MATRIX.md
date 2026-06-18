# Model Comparison Matrix

Data: 2026-06-18

| Modelo | Tipo | Entrada | Saida | Comparavel por F1 | Custo esperado | Uso no artigo |
|---|---|---|---|---|---|---|
| Logistic Regression | Classico supervisionado | Features normalizadas | Probabilidade/classe | Sim | Baixo | Baseline linear |
| Random Forest | Classico supervisionado | Features normalizadas | Probabilidade/classe | Sim | Baixo/medio | Baseline robusto nao linear |
| SVM-RBF | Classico supervisionado | Features normalizadas | Score/classe | Sim | Medio | Baseline kernel classico principal |
| Isolation Forest | Classico nao supervisionado | Features normalizadas | Score de anomalia/classe | Sim, via threshold interno | Baixo/medio | Baseline anomalia sem labels |
| QSVM-ZZ | QML kernel | PCA para `n_qubits` | Classe | Sim | Alto em simulador | Comparacao direta com SVM-RBF em baixa dimensao |
| QSVM-Pauli | QML kernel | PCA para `n_qubits` | Classe | Sim | Alto em simulador | Sensibilidade a feature map |
| VQC | QML variacional | PCA para `n_qubits` | Classe | Sim | Alto | Modelo hibrido treinavel |
| VQE Score | Hibrido/score Hamiltoniano | PCA para `n_qubits` | Score continuo, classe se threshold | Sim apenas com threshold | Medio/alto | Score fisicamente inspirado |
| FALQON | Controle/POC drift | Janelas temporais | Serie de recuperacao/degradacao | Parcial | Medio | Analise de concept drift |

## Observacoes por modelo

### Logistic Regression

Referencia simples e interpretavel. Deve ter baixo custo e servir para mostrar se o dataset e linearmente separavel com as features atuais.

### Random Forest

Baseline forte para tabular IDS. Deve ser usado como referencia classica principal ao lado de SVM-RBF.

### SVM-RBF

Baseline kernel classico mais importante para comparacao com QSVM. Deve ser reportado tambem em versao PCA quando comparado diretamente com QSVM.

### Isolation Forest

Util para anomalia sem labels. Deve ser identificado como baseline nao supervisionado, com cautela na comparacao contra classificadores supervisionados.

### QSVM-ZZ

Modelo QML kernel com ZZFeatureMap. Deve usar exatamente as mesmas features reduzidas que o SVM-RBF PCA baseline.

### QSVM-Pauli

Variante para medir impacto do feature map. Importante para discutir expressividade e custo de circuito.

### VQC

Modelo hibrido treinavel com curva de convergencia. Deve reportar otimizador, iteracoes, loss final e variancia entre seeds.

### VQE Score

Gera score Hamiltoniano continuo. So deve entrar em F1, precision e recall quando o threshold estiver configurado e registrado no manifesto/resumo.

### FALQON

Ainda e POC de concept drift. Nao deve ser vendido como classificador DDoS completo sem uma saida por amostra e protocolo de rotulagem temporal.

## Recomendacao de ranking

Separar rankings em tres grupos:

1. Classificadores supervisionados classicos.
2. Classificadores QML comparaveis.
3. POCs NISQ/hibridas com metricas especificas.

