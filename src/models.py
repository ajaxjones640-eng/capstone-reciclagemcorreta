"""Modelos e validação."""
from dataclasses import dataclass


@dataclass
class Item:
    """Exemplo de modelo — substitua pelos campos reais do domínio."""
    nome: str

    def validar(self) -> bool:
        return bool(self.nome and self.nome.strip())
