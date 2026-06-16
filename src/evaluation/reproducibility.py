from __future__ import annotations

import json
import subprocess
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path

import yaml


def dataset_name(config: dict) -> str:
    return str(config.get("dataset", {}).get("mode", "synthetic"))


def build_experiment_id(experiment_name: str | None = None) -> str:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    prefix = experiment_name.strip().replace(" ", "-") if experiment_name else "run"
    safe = "".join(ch for ch in prefix if ch.isalnum() or ch in {"-", "_"}).strip("-_")
    return f"{safe or 'run'}-{stamp}"


def git_commit_hash() -> str:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
        )
        return result.stdout.strip()
    except Exception:
        return "unknown"


def infer_backend(config: dict) -> str:
    try:
        import qiskit_algorithms  # noqa: F401
        import qiskit_aer  # noqa: F401

        return "qiskit_algorithms+qiskit_aer"
    except Exception:
        return "fallback-capable"


def manifest(config: dict, experiment_id: str, output_dir: str) -> dict:
    pre = config.get("preprocessing", {})
    exp = config.get("experiments", {})
    return {
        "experiment_id": experiment_id,
        "git_commit_hash": git_commit_hash(),
        "dataset": dataset_name(config),
        "seed": int(config.get("seed", 42)),
        "n_qubits": int(pre.get("n_qubits", 4)),
        "feature_map": exp.get("qsvm_feature_maps", ["zz"]),
        "optimizer": "COBYLA",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "backend": infer_backend(config),
        "output_dir": output_dir,
    }


def initialize_experiment(config: dict, config_path: str, experiment_name: str | None = None) -> dict:
    dataset = dataset_name(config)
    experiment_id = build_experiment_id(experiment_name)
    root = Path(config.get("experiments", {}).get("output_dir", "results"))
    output = root / dataset / experiment_id
    (output / "plots").mkdir(parents=True, exist_ok=True)
    (output / "artifacts").mkdir(parents=True, exist_ok=True)

    snapshot = deepcopy(config)
    snapshot.pop("_experiment", None)
    with open(output / "config_snapshot.yaml", "w", encoding="utf-8") as fh:
        yaml.safe_dump(snapshot, fh, sort_keys=False, allow_unicode=True)

    data = manifest(config, experiment_id, str(output))
    data["config_path"] = config_path
    with open(output / "experiment_manifest.json", "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2, sort_keys=True)

    config["_experiment"] = {
        "id": experiment_id,
        "dataset": dataset,
        "output_dir": str(output),
        "manifest": data,
    }
    return config
