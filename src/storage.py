"""Operações com JSON."""
import json
from pathlib import Path

DATA_FILE = Path("data.json")


def carregar() -> list:
    if not DATA_FILE.exists():
        return []
    with DATA_FILE.open("r", encoding="utf-8") as f:
        return json.load(f)


def salvar(dados: list) -> None:
    with DATA_FILE.open("w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)
