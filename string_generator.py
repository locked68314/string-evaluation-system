import random
import string
from dataclasses import dataclass
from typing import Optional, Union, Generator

@dataclass
class StringGeneratorConfig:
    length: Union[int, tuple[int, int]] = (50, 100)
    blank_spaces: Union[int, tuple[int, int]] = (3, 5) 
    count: int = 5
    seed: Optional[int] = None  # Para reproducibilidad

class StringGenerator:
    def __init__(self, config: StringGeneratorConfig):
        self.config = config
        self._setup_charset()
        if config.seed is not None:
            random.seed(config.seed)

    def _setup_charset(self):
        self.charset = string.ascii_letters + string.digits

    def _get_length(self) -> int:
        if isinstance(self.config.length, tuple):
            return random.randint(self.config.length[0], self.config.length[1])
        return self.config.length
    
    def _get_spaces(self) -> int:
        if isinstance(self.config.length, tuple):
            return random.randint(self.config.blank_spaces[0], self.config.blank_spaces[1])
        return self.config.blank_spaces
    
    def _get_space_positions(self, length: int, space_count: int) -> list[int]:
        """Devuelve posiciones válidas no consecutivas para espacios."""
        possible_positions = list(range(1, length - 1))  # Evitamos extremos
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
        for _ in range(self.config.count):
            yield self.generate_one()

    def write_to_file(self, file_path):
        with open(file_path, 'w') as file:
            file.write('\n'.join(self.generate_all()) + '\n')

if __name__ == "__main__":
    config = StringGeneratorConfig(length=(50, 100), count=10, blank_spaces=(3, 5), seed=None)
    generator = StringGenerator(config)
    for s in generator.generate_all():
        print(s)
