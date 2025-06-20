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
    """
    Manages and applies a list of rule objects to input strings.

    Iterates through all rules to determine whether a string should be ignored,
    and provides the reason for ignoring it.

    Attributes:
        reglas (list[BaseRule]): List of rule instances to apply.
    """
    def __init__(self, reglas: list[BaseRule]):
        """
        Args:
            reglas (list[BaseRule]): A list of rule objects implementing the BaseRule interface.
        """
        self.reglas = reglas

    def test_rules(self, cadena: str) -> str | None:
        """
        Checks if the input string should be ignored based on the configured rules.

        Evaluates all rules in order and returns the first matching rule's message.

        Args:
            cadena (str): The string to evaluate.

        Returns:
            str | None: A message from the matching rule, or None if the string is allowed.
        """
        for regla in self.reglas:
            if not regla.test_rule(cadena):
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