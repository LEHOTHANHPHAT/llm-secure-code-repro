"""Draft prompts for the pilot. Compare with the authors' prompts before freezing."""


def vanilla(instruction: str, entry_point: str) -> str:
    return (
        f"Implement this Python task:\n{instruction}\n\n"
        f"Use the entry point {entry_point}. Return only Python source code."
    )


def request_hints(instruction: str) -> str:
    return (
        f"Task:\n{instruction}\n\n"
        "List up to five security risks relevant to this task and how to avoid them. "
        "Prioritize the most relevant risks. Do not write the implementation."
    )


def guided(instruction: str, entry_point: str, hints: str) -> str:
    return f"{vanilla(instruction, entry_point)}\n\nConsider these hints:\n{hints}"


def request_explanation(code: str, diagnostic: str) -> str:
    return (
        "Explain the scanner finding, why it matters in this code, and suggest "
        "a concrete fix that preserves behavior. Return feedback, not a full patch.\n\n"
        f"Code:\n{code}\n\nScanner finding:\n{diagnostic}"
    )


def repair(instruction: str, entry_point: str, code: str, feedback: str) -> str:
    return (
        f"{vanilla(instruction, entry_point)}\n\n"
        f"Original code:\n{code}\n\nFeedback:\n{feedback}\n\n"
        "Fix the issue while preserving the requested behavior and function signature."
    )
