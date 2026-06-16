from __future__ import annotations

from src.evaluation.reports import append_rows
from src.experiments.common import finish, load_and_initialize, output_dir, parse_args, prepared_quantum, reset_outputs
from src.quantum.qaoa_graph import run_qaoa_maxcut


def run(config: dict):
    X_train, y_train, _, _, warnings = prepared_quantum(config)
    row = run_qaoa_maxcut(X_train, output_dir(config), int(config.get("experiments", {}).get("qaoa_nodes", 8)))
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
