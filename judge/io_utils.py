def confirm_reuse(path, label: str) -> bool:
    answer = input(f"{label} already exists at {path}. Use existing? [Y/n] ").strip().lower()
    return answer != "n"
