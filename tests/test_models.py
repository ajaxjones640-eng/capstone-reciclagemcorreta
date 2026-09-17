"""Testes unitários iniciais."""
import unittest

from src.models import Item


class TestItem(unittest.TestCase):
    def test_validar_ok(self):
        self.assertTrue(Item(nome="Exemplo").validar())

    def test_validar_vazio(self):
        self.assertFalse(Item(nome="").validar())


if __name__ == "__main__":
    unittest.main()
