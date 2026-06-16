from __future__ import annotations

from src.classical.autoencoder import run_classical_autoencoder
from src.classical.baselines import run_classical_baselines
from src.experiments.common import finish, load_and_initialize, output_dir, parse_args, prepared_classical, reset_outputs


def run(config: dict):
    X_train, X_test, y_train, y_test, warnings = prepared_classical(config)
    threshold = float(config.get("experiments", {}).get("alert_threshold", 0.5))
    seed = int(config.get("seed", 42))
    rows = run_classical_baselines(X_train, X_test, y_train, y_test, threshold, seed)
    rows.append(run_classical_autoencoder(X_train, X_test, y_train, y_test, seed=seed))
    return rows, warnings


def main():
    args = parse_args()
    config = load_and_initialize(args)
    out = output_dir(config)
    if args.reset:
        reset_outputs(out)
    rows, warnings = run(config)
    from src.evaluation.reports import append_rows

    append_rows(out, rows)
    finish(out, warnings)


if __name__ == "__main__":
    main()
