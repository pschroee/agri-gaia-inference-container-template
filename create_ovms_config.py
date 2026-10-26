# SPDX-FileCopyrightText: 2026 Philipp Schröer
# SPDX-License-Identifier: MIT
"""Write the OpenVINO Model Server configuration for a model repository.

Every sub directory <name> of the repository must hold <name>/1/model.onnx.
The script writes <repository>/config.json that serves each model on the CPU.
"""
import argparse
import json
import os
import sys


def get_args():
    parser = argparse.ArgumentParser(description="Write config.json for OVMS.")
    parser.add_argument(
        "--repository",
        type=str,
        default="model_repository",
        help="Path to the model repository.",
    )
    return parser.parse_args()


def main():
    args = get_args()
    repository = args.repository

    names = sorted(
        d for d in os.listdir(repository) if os.path.isdir(os.path.join(repository, d))
    )
    models = []
    for name in names:
        if not os.path.isfile(os.path.join(repository, name, "1", "model.onnx")):
            print(
                f"error: {name} has no 1/model.onnx; "
                "the OVMS template serves ONNX models only",
                file=sys.stderr,
            )
            sys.exit(1)
        models.append(
            {
                "config": {
                    "name": name,
                    "base_path": f"/model_repository/{name}",
                    "target_device": "CPU",
                    "plugin_config": {"INFERENCE_PRECISION_HINT": "f32"},
                }
            }
        )

    with open(os.path.join(repository, "config.json"), "w") as file:
        json.dump({"model_config_list": models}, file, indent=2)
        file.write("\n")


if __name__ == "__main__":
    main()
