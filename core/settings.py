import pathlib
from typing import Final, TypeAlias

T_ALPHABET: TypeAlias = str
T_ALPHABETS: TypeAlias = list[T_ALPHABET]
T_FILE_NAME: TypeAlias = str
T_TXT_FILE_NAME: TypeAlias = str
T_JSON_FILE_NAME: TypeAlias = str

ROOT_PATH: Final[pathlib.Path] = pathlib.Path(__file__).parents[1]
OUTPUT_PATH: Final[pathlib.Path] = ROOT_PATH.joinpath('results')
INPUT_PATH: Final[pathlib.Path] = ROOT_PATH.joinpath('app/input_alphabets.txt')
