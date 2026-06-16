from __future__ import annotations

from pathlib import Path
import pandas as pd


def append_rows(output_dir: str, rows: list[dict]):
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    path = Path(output_dir) / "metrics.csv"
    df = pd.DataFrame(rows)
    if path.exists():
        df = pd.concat([pd.read_csv(path), df], ignore_index=True)
    df.to_csv(path, index=False)


def record_failure(output_dir: str, experiment: str, error: str):
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    path = Path(output_dir) / "failures.csv"
    row = pd.DataFrame([{"experiment": experiment, "error": error}])
    if path.exists():
        row = pd.concat([pd.read_csv(path), row], ignore_index=True)
    row.to_csv(path, index=False)


def write_summary(output_dir: str, warnings: list[str] | None = None):
    out = Path(output_dir)
    metrics_path = out / "metrics.csv"
    failures_path = out / "failures.csv"
    lines = ["# AnomaliQ v3 - Relatório Experimental", ""]
    lines.append("Suíte reprodutível para detecção adaptativa de DDoS com modelos clássicos, QML e POCs híbridas em ambiente NISQ.")
    lines.append("")
    if metrics_path.exists():
        df = pd.read_csv(metrics_path)
        lines.append("## Métricas coletadas")
        table = df.sort_values("f1", ascending=False, na_position="last") if "f1" in df.columns else df
        try:
            lines.append(table.to_markdown(index=False))
        except Exception:
            lines.append("```")
            lines.append(table.to_string(index=False))
            lines.append("```")
        lines.append("")
    if warnings:
        lines.append("## Avisos")
        lines.extend(f"- {w}" for w in warnings)
        lines.append("")
    lines.append("## Limitações")
    lines.append("- QAE completo e FALQON completo são interfaces POC; quando a dependência quântica não existe, usam fallback documentado.")
    lines.append("- QAOA usa solução exata por força bruta para grafos pequenos quando `qiskit_algorithms` não está instalado.")
    lines.append("- Simulação ruidosa usa Aer apenas se disponível; caso contrário, registra degradação aproximada por perturbação controlada.")
    if failures_path.exists():
        lines.append("")
        lines.append("## Falhas registradas")
        failures = pd.read_csv(failures_path)
        try:
            lines.append(failures.to_markdown(index=False))
        except Exception:
            lines.append("```")
            lines.append(failures.to_string(index=False))
            lines.append("```")
    (out / "summary.md").write_text("\n".join(lines), encoding="utf-8")
