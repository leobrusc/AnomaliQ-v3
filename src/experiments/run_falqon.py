from __future__ import annotations

from src.evaluation.reports import append_rows
from src.experiments.common import finish, load_config, output_dir, parse_args, prepared_classical, reset_outputs
from src.quantum.falqon_drift import run_falqon_drift


def run(config: dict):
    X_train, X_test, y_train, y_test, warnings = prepared_classical(config)
    row = run_falqon_drift(X_train, X_test, y_train, y_test, output_dir(config), int(config.get("experiments", {}).get("falqon_windows", 6)), int(config.get("seed", 42)))
    return [row], warnings


def main():
    args = parse_args()
    config = load_config(args.config)
    out = output_dir(config)
    if args.reset:
        reset_outputs(out)
    rows, warnings = run(config)
    append_rows(out, rows)
    finish(out, warnings)


if __name__ == "__main__":
    main()
