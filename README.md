# AnomaliQ v3

**Framework Hamiltoniano Híbrido para Detecção Adaptativa de Ataques DDoS utilizando Quantum Machine Learning em Ambientes NISQ**

> Brazil Quantum Camp — 2026

---

## Visão Geral

O **AnomaliQ v3** é uma arquitetura híbrida clássico-quântica baseada em algoritmos variacionais e modelagem Hamiltoniana para detecção adaptativa de ataques DDoS em tráfego HTTP.

O tráfego de rede é modelado como um sistema físico quântico, onde:
- **baixa energia** → tráfego legítimo
- **estados excitados** → ataques DDoS

---

## Arquitetura

```
Tráfego HTTP
     │
     ▼
Pré-processamento (StandardScaler + PCA)
     │
     ▼
Quantum Feature Encoding (ZZFeatureMap)
     │
     ├──▶ QSVM — Classificação por kernel quântico
     ├──▶ VQC  — Classificador variacional
     ├──▶ VQE  — Score energético de anomalia
     ├──▶ QAOA — Clusterização de tráfego
     └──▶ FALQON — Adaptação temporal (concept drift)
     │
     ▼
Geração de Alertas
```

---

## Algoritmos Quânticos

| Algoritmo | Função |
|-----------|--------|
| QSVM | Classificação via kernel quântico |
| VQC | Classificação variacional híbrida |
| VQE | Score energético de anomalia |
| QAOA | Clusterização e detecção de comunidades anômalas |
| FALQON | Adaptação temporal e mitigação de concept drift |

---

## Instalação

```bash
# Clone o repositório
git clone https://github.com/leobrusc/AnomaliQ-v3.git
cd AnomaliQ-v3

# Crie e ative o ambiente virtual
python -m venv .venv
.venv\Scripts\Activate.ps1  # Windows

# Instale as dependências
pip install -r requirements.txt
```

---

## Estrutura do Projeto

```
AnomaliQ-v3/
├── src/
│   ├── preprocessing.py     # Normalização e redução dimensional
│   ├── feature_map.py       # Quantum Feature Maps
│   ├── qsvm.py              # Quantum SVM
│   ├── vqc.py               # Variational Quantum Classifier
│   ├── vqe_score.py         # Score energético via VQE
│   ├── qaoa_cluster.py      # Clusterização via QAOA
│   ├── falqon.py            # Adaptação temporal FALQON
│   └── alerts.py            # Geração de alertas
├── notebooks/
│   └── experiment_01.ipynb  # Experimento inicial
├── data/
├── figures/
├── results/
├── requirements.txt
└── README.md
```

---

## Datasets

| Dataset | Aplicação |
|---------|-----------|
| CICIDS2017 | Intrusion Detection |
| UNSW-NB15 | Segurança de Rede |
| TON_IoT | IoT Security |
| HTTP CSIC 2010 | Tráfego HTTP |
| CSE-CIC-IDS2018 | IDS Moderno |

---

## Métricas

- **ML:** Accuracy, Precision, Recall, F1-Score, ROC-AUC, MCC
- **Segurança:** Detection Rate, False Positive Rate, Time-to-Detection
- **Quânticas:** Fidelidade, Profundidade de Circuito, Entanglement Capability
- **Índice Híbrido:** Quantum Security Index (QSI)

---

## Referências

- Biamonte et al. — Quantum Machine Learning. *Nature*, 2017.
- Havlíček et al. — Supervised Learning with Quantum-Enhanced Feature Spaces. *Nature*, 2019.
- Cerezo et al. — Variational Quantum Algorithms. *Nature Reviews Physics*, 2021.
- Zargar et al. — A Survey of Defense Mechanisms Against DDoS Flooding Attacks. *IEEE*, 2013.

---

## Licença

MIT License — Brazil Quantum Camp 2026
