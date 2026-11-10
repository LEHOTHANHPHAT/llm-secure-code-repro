"""Load a JSONL manifest. Evaluation labels stay separate from prompt inputs."""

import json
import re
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Task:
    task_id: str
    source: str
    source_id: str
    target_cwe: str
    instruction: str
    entry_point: str


def load_tasks(path: Path) -> list[Task]:
    tasks = []
    seen_ids = set()
    with path.open(encoding="utf-8-sig") as stream:
        for number, line in enumerate(stream, 1):
            if not line.strip():
                continue
            try:
                task = Task(**json.loads(line))
                if any(not isinstance(value, str) or not value.strip()
                       for value in vars(task).values()):
                    raise ValueError("Các trường phải là chuỗi có nội dung")
                if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]*", task.task_id):
                    raise ValueError("task_id chứa ký tự không hợp lệ")
                if not re.fullmatch(r"CWE-[1-9][0-9]*", task.target_cwe):
                    raise ValueError("target_cwe phải có dạng CWE-22")
                if not task.entry_point.isidentifier():
                    raise ValueError("entry_point phải là tên hàm Python")
                if task.task_id in seen_ids:
                    raise ValueError(f"task_id bị trùng: {task.task_id}")
            except (TypeError, ValueError) as error:
                raise ValueError(f"{path}:{number}: {error}") from error
            seen_ids.add(task.task_id)
            tasks.append(task)
    if not tasks:
        raise ValueError(f"{path}: bộ dữ liệu rỗng")
    return tasks
