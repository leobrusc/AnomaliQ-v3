from __future__ import annotations

from src.evaluation.reports import append_rows
from src.experiments.common import finish, load_and_initialize, output_dir, parse_args, prepared_classical, reset_outputs
from src.quantum.qae import run_qae_placeholder


def run(config: dict):
    X_train, X_test, y_train, y_test, warnings = prepared_classical(config)
    return [run_qae_placeholder(X_train, X_test, y_train, y_test, int(config.get("seed", 42)))], warnings


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
