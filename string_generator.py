import random
import string
from dataclasses import dataclass
from typing import Optional, Union, Generator

@dataclass
class StringGeneratorConfig:
    """Configuration for the string generator.

    Attributes:
        length (int | tuple[int, int]): Fixed length or range of string length.
        blank_spaces (int | tuple[int, int]): Fixed or range of blank spaces to insert.
        count (int): Number of strings to generate.
        seed (Optional[int]): Optional random seed for reproducibility.
    """
    length: Union[int, tuple[int, int]] = (50, 100)
    blank_spaces: Union[int, tuple[int, int]] = (3, 5) 
    count: int = 5 
    seed: Optional[int] = None

class StringGenerator:
    """Generates random strings composed of letters, digits, and non-consecutive spaces."""
    def __init__(self, config: StringGeneratorConfig):
        """Initializes the generator with the given configuration.

        Args:
            config (StringGeneratorConfig): Generator parameters.
        """
        self.config = config
        self._setup_charset()
        if config.seed is not None:
            random.seed(config.seed)

    def _setup_charset(self):
        """Initializes the character set used for string generation (a-zA-Z0-9)."""
        self.charset = string.ascii_letters + string.digits

    def _get_length(self) -> int:
        """Returns a randomly chosen length based on the config.

        Returns:
            int: The string length.
        """
        if isinstance(self.config.length, tuple):
            return random.randint(self.config.length[0], self.config.length[1])
        return self.config.length
    
    def _get_spaces(self) -> int:
        """Returns a randomly chosen number of spaces based on the config.

        Returns:
            int: Number of blank spaces.
        """
        if isinstance(self.config.blank_spaces, tuple):
            return random.randint(self.config.blank_spaces[0], self.config.blank_spaces[1])
        return self.config.blank_spaces
    
    def _get_space_positions(self, length: int, space_count: int) -> list[int]:
        """Determines valid, non-consecutive positions for inserting spaces.

        Avoids placing spaces at the beginning or end, and ensures they are not consecutive.

        Args:
            length (int): Length of the string.
            space_count (int): Number of spaces to place.

        Returns:
            list[int]: Sorted list of positions for spaces.

        Raises:
            ValueError: If not enough valid positions are available.
        """
        possible_positions = list(range(1, length - 1))  # avoids ends
        random.shuffle(possible_positions)

        space_positions = []
        for pos in possible_positions:
            if all(abs(pos - s) > 1 for s in space_positions):
                space_positions.append(pos)
            if len(space_positions) == space_count:
                break

        if len(space_positions) < space_count:
            raise ValueError("No se pudieron ubicar suficientes espacios no consecutivos.")

        return sorted(space_positions)
    
    def generate_one(self) -> str:
        # genera una cadena en base a la configuracion y la devuelve
        length = self._get_length()
        space_count = self._get_spaces()
        if length < space_count + (space_count - 1):
            raise ValueError(f"Longitud {length} insuficiente para incluir {space_count} espacios no consecutivos.")

        space_positions = self._get_space_positions(length, space_count)
        result = []

        for i in range(length):
            if i in space_positions:
                result.append(" ")
            else:
                result.append(random.choice(self.charset))

        return ''.join(result)

    def generate_all(self) -> Generator[str, None, None]:
        """Generates a single string with the configured length and spaces.

        Returns:
            str: A randomly generated string.

        Raises:
            ValueError: If the length is too short to include the requested number of spaces.
        """
        for _ in range(self.config.count):
            yield self.generate_one()

    def write_to_file(self, file_path):
        """Writes all generated strings to a file.

        Args:
            file_path (str): Path to the output file.
        """
        with open(file_path, 'w') as file:
            file.write('\n'.join(self.generate_all()) + '\n')

if __name__ == "__main__":
    # Usage example: generates 10 lines each with a random length between 50 and 100 characters, each with 3 or 5 spaces
    config = StringGeneratorConfig(length=(50, 100), count=10, blank_spaces=(3, 5), seed=None)
    generator = StringGenerator(config)
    for s in generator.generate_all():
        print(s)
