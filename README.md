# agri-gaia-inference-container-template

## Branch ovms-onnx

This branch serves ONNX models with [OpenVINO Model Server](https://github.com/openvinotoolkit/model_server) instead of Triton.

- CPU only (`target_device CPU`), amd64 only, ONNX models only.
- The model repository layout is the same as on the `triton` branch (`<name>/1/model.onnx`); `create_ovms_config.py` adds `model_repository/config.json`.
- KServe v2 over HTTP on port 8000 and gRPC on port 8001. There is no metrics port.
- Precision hint `f32` (also on CPUs with BF16, so the results match the ONNX reference).
- The base image `openvino/model_server:2026.4.1` is pinned by digest (Apache-2.0).
