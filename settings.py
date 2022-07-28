import string
from typing import Final

path_for_links: Final[str] = 'found_links.json'

ALPHABET: Final[str] = ''.join([
    # string.ascii_lowercase,
    # string.ascii_uppercase,
    string.digits,
])
