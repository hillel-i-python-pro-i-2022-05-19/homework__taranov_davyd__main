import logging
from datetime import datetime

from core.settings import T_ALPHABET
from tools.utils import _write_json_words_file_for_app, creat_file_name


class FuzzGenerator:
    def __init__(self, alphabet: T_ALPHABET, words_count: int, word_length: int):
        self.alphabet = alphabet
        self.words_count = words_count
        self.word_length = word_length
        self.words_as_list = []

    def words_generator(self) -> None:
        # there is a description of the work in README.md
        start_time = datetime.now()
        basic_symbols_of_alphabet_as_list = list(self.alphabet)
        logging.info(f'start - words: {len(self.words_as_list)}')
        for basic_symbol in basic_symbols_of_alphabet_as_list:
            if len(self.words_as_list) == self.words_count:
                break
            if len(basic_symbol) < self.word_length:
                for _ in range(self.word_length - 1):
                    basic_symbol += self.alphabet[0]
            elif self.word_length == 1:
                basic_symbol = basic_symbol
            self.words_as_list.append(basic_symbol[::-1])

        break_bool = True
        for copy_word in self.words_as_list:
            if break_bool == False:
                break
            if copy_word != self.alphabet[0] * self.word_length:
                for symbol in self.alphabet:
                    final_word = ''.join([copy_word, str(symbol)])
                    final_word = final_word[len(final_word) - self.word_length:]
                    if final_word in self.words_as_list or len(self.words_as_list) == self.words_count:
                        break_bool = False
                        break
                    self.words_as_list.append(final_word)
                    logging.info(f'word: "{final_word}" add to file')

        logging.info(f'end - words: {len(self.words_as_list)}')
        logging.info(datetime.now() - start_time)
        file_name = creat_file_name(self.alphabet, len(self.words_as_list), self.word_length)
        _write_json_words_file_for_app(file_name=file_name, words=self.words_as_list)
