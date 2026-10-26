# SPDX-FileCopyrightText: 2026 Philipp Schröer
# SPDX-License-Identifier: MIT
# Branch ovms-onnx: serves ONNX models with OpenVINO Model Server (CPU, amd64).
FROM python:3.12-slim as build_stage
WORKDIR /work

RUN pip install jinja2~=3.0.3
COPY model_config_template.pbtxt .
COPY create_triton_model_repository.py .
COPY create_ovms_config.py .

COPY models /work/models
RUN python3 create_triton_model_repository.py --use-autoconfig
RUN python3 create_ovms_config.py

FROM openvino/model_server:2026.4.1@sha256:148e3fe802261ed0b5b634de3bbccdefe7176a218ec34a88e382b40704c34a1c

COPY --from=build_stage /work/model_repository /model_repository

CMD ["--config_path", "/model_repository/config.json", "--rest_port", "8000", "--port", "8001"]
