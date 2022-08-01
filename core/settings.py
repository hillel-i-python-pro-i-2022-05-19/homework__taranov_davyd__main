from typing import Final, TypeAlias

T_ALPHABET: TypeAlias = str
T_ALPHABETS: TypeAlias = list[T_ALPHABET]
T_FILE_NAME: TypeAlias = str
T_TXT_FILE_NAME: TypeAlias = str
T_JSON_FILE_NAME: TypeAlias = str

path_for_alphabets: Final[str] = 'app/input_alphabets.txt'
