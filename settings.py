import string
from typing import Final, TypeAlias

path_input_links: Final[str] = 'input_links.txt'
T_URL: TypeAlias = str or list
T_URLS: TypeAlias = list[T_URL]
T_HTML_TEXT: TypeAlias = str

ALPHABET: Final[str] = ''.join([
    # string.ascii_lowercase,
    # string.ascii_uppercase,
    string.digits,
])
