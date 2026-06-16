from __future__ import annotations

from src.evaluation.reports import append_rows
from src.experiments.common import finish, load_and_initialize, output_dir, parse_args, reset_outputs, run_and_record
from src.quantum.nisq_noise import benchmark_noise


def main():
    args = parse_args()
    config = load_and_initialize(args)
    out = output_dir(config)
    reset_outputs(out)
    warnings = []

    from src.experiments import run_baselines, run_falqon, run_qae, run_qaoa, run_qsvm, run_vqc, run_vqe

    for name, module in [
        ("baselines", run_baselines),
        ("qsvm", run_qsvm),
        ("vqc", run_vqc),
        ("qae", run_qae),
        ("vqe", run_vqe),
        ("qaoa", run_qaoa),
        ("falqon", run_falqon),
    ]:
        warnings.extend(run_and_record(config, name, module.run))

    try:
        from src.experiments.common import prepared_quantum

        X_train, y_train, X_test, y_test, _ = prepared_quantum(config)
        df = benchmark_noise(X_train, X_test, y_train, y_test, out, config.get("experiments", {}).get("noise_levels", [0.0, 0.05, 0.1]), int(config.get("seed", 42)))
        best = df.iloc[0].to_dict()
        worst = df.iloc[-1].to_dict()
        append_rows(out, [{"model": "NISQ noise benchmark", "f1": worst["f1"], "f1_degradation_under_noise": worst["f1_degradation_under_noise"], "n_qubits": int(config.get("preprocessing", {}).get("n_qubits", 4)), "simulator": worst["simulator"]}])
    except Exception as exc:
        from src.evaluation.reports import record_failure

        record_failure(out, "nisq_noise", repr(exc))

    finish(out, warnings)


if __name__ == "__main__":
    main()
