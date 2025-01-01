from abc import ABC, abstractmethod
from pathlib import Path

import pytest
import yaml

from src.data.state import State
from src.data import exceptions
from src.game import Game


class Action(ABC):

    @abstractmethod
    def __call__(self, game: Game):
        pass

class Move(Action):

    def __init__(self, index: int, error: str = ""):
        self.index = index
        self.error = error

    def __call__(self, game: Game):
        if self.error:
            exception = getattr(exceptions, to_upper(self.error))
            with pytest.raises(exception):
                game.play(self.index)
        else:
            game.play(self.index)

class CheckState(Action):

    def __init__(self, state: str):
        self.state = State.from_str(state)

    def __call__(self, game: Game):
        assert game.state == self.state

def init_game(yaml_file_data: dict) -> Game | None:
    if error := yaml_file_data.get("game", {}).get("error", ""):
        if yaml_file_data.get("actions"):
            raise ValueError("Game with error shouldn't have actions.")
        del yaml_file_data["game"]["error"]
        exception = getattr(exceptions, to_upper(error))
        with pytest.raises(exception):
            Game(**yaml_file_data.get("game", {}))
        return None
    return Game(**yaml_file_data.get("game", {}))


def all_yaml_files() -> list[Path]:
    yaml_dir = Path(__file__).parent / "yaml_test_case"
    return list(yaml_dir.rglob("*.yaml"))


def load_test_case(yaml_file: Path):
    with open(yaml_file, 'r') as file:
        return yaml.safe_load(file)


def to_pascal(value: str) -> str:
    return value.replace(" ", "_").upper()

def to_upper(value: str) -> str:
    return value.replace("_", " ").title().replace(" ", "").replace("Ai", "AI")


@pytest.mark.parametrize("yaml_file", all_yaml_files(), ids=[file.name for file in all_yaml_files()])
def test_yaml_test_case(yaml_file: Path):
    data = load_test_case(yaml_file)
    game: Game | None = init_game(data)

    if not game:
        return

    for index, action_data in enumerate(data.get("actions", [])):
        print(f"Start action: {index + 1}")
        print("Action data:", action_data)
        action_type = to_upper(action_data["type"])
        del action_data["type"]
        action = globals()[action_type](**action_data)
        action(game)
