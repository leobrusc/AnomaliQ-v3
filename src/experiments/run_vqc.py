from __future__ import annotations

from src.evaluation.reports import append_rows
from src.experiments.common import finish, load_and_initialize, output_dir, parse_args, prepared_quantum, reset_outputs
from src.quantum.vqc import run_vqc


def run(config: dict):
    X_train, y_train, X_test, y_test, warnings = prepared_quantum(config)
    exp = config.get("experiments", {})
    row = run_vqc(
        X_train,
        X_test,
        y_train,
        y_test,
        int(config.get("preprocessing", {}).get("n_qubits", 4)),
        int(exp.get("vqc_maxiter", 25)),
        output_dir(config),
        float(exp.get("alert_threshold", 0.5)),
        int(config.get("seed", 42)),
    )
    return [row], warnings


def main():
    args = parse_args()
    config = load_and_initialize(args)
    out = output_dir(config)
    if args.reset:
        reset_outputs(out)
    rows, warnings = run(config)
    append_rows(out, rows)
    finish(out, warnings)


if __name__ == "__main__":
    main()
