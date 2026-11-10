"""Validate an experiment manifest and preview the jobs it describes."""

import argparse
import json
from collections import Counter
from pathlib import Path

from .dataset import load_tasks
from .prompts import request_hints, vanilla


def plan(config_path: Path) -> dict:
    config = json.loads(config_path.read_text(encoding="utf-8-sig"))
    tasks = load_tasks(config_path.parent / config["dataset"])
    counts = Counter(task.target_cwe for task in tasks)
    if dict(counts) != config["expected_cwe_counts"]:
        raise ValueError(f"Số bài theo CWE không đúng cấu hình: {dict(counts)}")

    models = config["models"]
    if (not isinstance(models, list) or len(models) != 2
            or any(not isinstance(model, str) or not model.strip() for model in models)
            or len(set(models)) != 2):
        raise ValueError("Cấu hình phải có hai model ID phân biệt")
    repeat = config["repeats"]
    if type(repeat) is not int or repeat < 1:
        raise ValueError("repeats phải là số nguyên dương")

    jobs = [
        {"task_id": task.task_id, "model_id": model, "repeat_id": attempt}
        for task in tasks
        for model in models
        for attempt in range(1, repeat + 1)
    ]
    return {
        "mode": "plan_only",
        "tasks_by_cwe": dict(counts),
        "generation_pairs": len(jobs),
        "generation_and_hint_calls_planned": 3 * len(jobs),
        "repair": "R1/R2 start from the same B0 code only when B0 has a scanner finding.",
        "first_job": jobs[0],
        "first_b0_prompt": vanilla(tasks[0].instruction, tasks[0].entry_point),
        "first_hint_prompt": request_hints(tasks[0].instruction),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    planner = commands.add_parser("plan", help="Validate inputs and preview the experiment")
    planner.add_argument("--config", type=Path, default=Path("configs/smoke.json"))
    args = parser.parse_args()
    try:
        result = plan(args.config)
    except (OSError, ValueError, KeyError, TypeError) as error:
        parser.exit(1, f"Lỗi cấu hình hoặc dữ liệu: {error}\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
