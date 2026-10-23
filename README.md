# Motion Challenge · sonic

[sonic](https://github.com/NVlabs/GR00T-WholeBodyControl) checkpoint adapter. G1 29DoF; LAFAN40 is the first suite.

## Install and run

```sh
git clone --recurse-submodules https://github.com/motion-challenge-project/motion-challenge-sonic.git
cd motion-challenge-sonic
uv sync
uv run evaluate.py
```

Reuses local `checkpoints/policy.onnx` or the external cache; missing artifacts are
fetched and hash-checked. Use `--weights PATH --data PATH --offline` for local files.
Results and traces are written outside Git. `--help` lists options.

The root `motion-challenge` submodule owns data, physics, metrics and verification.
This repository only adapts model inference; no `sim2real` dependency.

**Development adapter — author-inference review pending.**
[Provenance](provenance.json)

MuJoCo 3.17 batch is the default. Use `--jobs 8` for parallel clips;
download and evaluation progress updates every 5 seconds.

Run all frames after tracking failure: `uv run evaluate.py --termination none`.
This records full-motion errors under a separate protocol; success still requires no failure.

## Checkpoint source

[NVlabs/GR00T-WholeBodyControl](https://github.com/NVlabs/GR00T-WholeBodyControl/blob/45c03facbf848e0c743091b7d9c17952096ff908/README.md) · [policy.onnx (converted deployment artifact)](https://drive.google.com/file/d/1dRMw3SUUXPr4yFI0e8fcO9xGlVKtQxZI/view). Third-party export; equivalence not established.

This adapter uses an ONNX export from a shared deployment archive. The upstream project link alone does not authenticate this converted file; the original-to-export conversion and equivalence evidence are not yet complete. Results are withheld.
