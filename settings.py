import string
from typing import Final

path_for_links: Final[str] = 'found_links.json'
path_for_words: Final[str] = 'found_words.json'
url: Final[str or list[str]] = ['https://www.ted.com/talks/jay_walker_the_world_s_english_mania',
                                'https://python-scripts.com/threading']

ALPHABET: Final[str] = ''.join([
    # string.ascii_lowercase,
    # string.ascii_uppercase,
    string.digits,
])
