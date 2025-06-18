from abc import ABC, abstractmethod

class BaseRule(ABC):
    @abstractmethod
    def is_valid(self, cadena: str) -> bool:
        pass

class RuleManager:
    def __init__(self, reglas: list[BaseRule]):
        self.reglas = reglas

    def test_rules(self, cadena: str) -> str | None:
        for regla in self.reglas:
            if not regla.is_valid(cadena):
                return regla.message
        return None

class StartsWithRule(BaseRule):
    def __init__(self, prefix: str, message: str, ignore_case: bool = True,):
        self.prefix = prefix
        self.ignore_case = ignore_case
        self.message = message

    def is_valid(self, cadena: str) -> bool:
        if self.ignore_case:
            cadena = cadena.lower()
        return not cadena.startswith(self.prefix)