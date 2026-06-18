# CICIDS2017 Dataset Profile

Data: 2026-06-18

## Fonte local

Diretorio analisado:

```text
data/raw/cicids2017/
```

Arquivos originais encontrados:

```text
GeneratedLabelledFlows.zip
MachineLearningCSV.zip
```

O benchmark tabular usa os CSVs extraidos de `MachineLearningCSV.zip`.

## CSVs encontrados

| Arquivo | Linhas | Coluna de rotulo | Tamanho |
|---|---:|---|---:|
| `Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv` | 225745 | ` Label` | 77,123,859 bytes |
| `Friday-WorkingHours-Afternoon-PortScan.pcap_ISCX.csv` | 286467 | ` Label` | 76,906,168 bytes |
| `Friday-WorkingHours-Morning.pcap_ISCX.csv` | 191033 | ` Label` | 58,316,725 bytes |
| `Monday-WorkingHours.pcap_ISCX.csv` | 529918 | ` Label` | 176,927,918 bytes |
| `Thursday-WorkingHours-Afternoon-Infilteration.pcap_ISCX.csv` | 288602 | ` Label` | 83,102,436 bytes |
| `Thursday-WorkingHours-Morning-WebAttacks.pcap_ISCX.csv` | 170366 | ` Label` | 52,023,263 bytes |
| `Tuesday-WorkingHours.pcap_ISCX.csv` | 445909 | ` Label` | 135,078,995 bytes |
| `Wednesday-workingHours.pcap_ISCX.csv` | 692703 | ` Label` | 225,166,395 bytes |

Resumo:

- Total de CSVs: 8
- Tamanho total dos CSVs: 884,645,759 bytes
- Total de linhas: 2,830,743
- Numero de colunas: 79
- Coluna de rotulo detectada: ` Label`

## Colunas

As colunas originais incluem 78 features de fluxo e uma coluna de rotulo. Exemplos:

- ` Destination Port`
- ` Flow Duration`
- ` Total Fwd Packets`
- ` Total Backward Packets`
- `Total Length of Fwd Packets`
- `Flow Bytes/s`
- ` Flow Packets/s`
- ` Packet Length Std`
- `Init_Win_bytes_forward`
- ` Label`

O loader normaliza os nomes internamente para lowercase com `_`, removendo espacos e caracteres especiais.

## Distribuicao de classes global

| Classe | Amostras |
|---|---:|
| BENIGN | 2,273,097 |
| DoS Hulk | 231,073 |
| PortScan | 158,930 |
| DDoS | 128,027 |
| DoS GoldenEye | 10,293 |
| FTP-Patator | 7,938 |
| SSH-Patator | 5,897 |
| DoS slowloris | 5,796 |
| DoS Slowhttptest | 5,499 |
| Bot | 1,966 |
| Web Attack Brute Force | 1,507 |
| Web Attack XSS | 652 |
| Infiltration | 36 |
| Web Attack Sql Injection | 21 |
| Heartbleed | 11 |

## Cenario binario BENIGN vs DDoS

O benchmark atual filtra apenas:

| Classe binaria | Rotulo | Amostras globais |
|---|---:|---:|
| BENIGN | 0 | 2,273,097 |
| DDoS | 1 | 128,027 |

Total antes do limite por classe:

```text
2,401,124 amostras
```

Para o benchmark inicial publicavel desta branch, `configs/cicids_ddos_real_strict.yaml` usa:

```yaml
max_samples_per_class: 1000
```

Assim, cada seed trabalha com ate 1000 BENIGN e 1000 DDoS antes do split estratificado.

## Validacoes realizadas

- Os CSVs reais existem sob `data/raw/cicids2017/MachineLearningCVE/`.
- A descoberta do loader foi ajustada para busca recursiva com `Path.rglob("*.csv")`.
- Todos os CSVs possuem coluna de rotulo detectavel como `Label` apos normalizacao.
- O modo strict nao usa fallback sintetico.

