from abc import ABC, abstractmethod

class BaseRule(ABC):
    """
    Abstract base class for string filtering rules.

    Subclasses must implement logic to decide whether a string
    should be ignored and provide a custom message.

    Methods:
        test_rule(cadena): returns True if the string passes the rule.
    """
    @abstractmethod
    def test_rule(self, cadena: str) -> bool:
        """
        Determines whether the given string passes the rule.

        Args:
            cadena (str): The input string.

        Returns:
            bool: True if the string passes the rule.
        """
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
    """
    Ignores strings that start with a given prefix.

    Useful for filtering based on forbidden prefixes like 'aa', 'zz', etc.
    Case sensitivity can be toggled.

    Attributes:
        prefix (str): The prefix to check.
        ignore_case (bool): Whether the check is case-insensitive.
        message (str): The message to return if the rule is violated.
    """
    def __init__(self, prefix: str, message: str, ignore_case: bool = True,):
        """
        Initializes the rule with a prefix, message, and case sensitivity

        Args:
            prefix (str): The prefix to check.
            message (str): The message  to use if the string is not valid
            ignore_case (bool): Whether the check is case-insensitive. 
        """
        self.prefix = prefix
        self.ignore_case = ignore_case
        self.message = message

    def test_rule(self, cadena: str) -> bool:
        """
        Checks if the string starts with the specified prefix.

        Args:
            cadena (str): The input string.
        Returns:
            bool: True if the string passes the rule
        """
        if self.ignore_case:
            cadena = cadena.lower()
        return not cadena.startswith(self.prefix)