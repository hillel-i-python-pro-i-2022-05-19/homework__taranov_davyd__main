import concurrent.futures
import logging
from datetime import datetime

from core.settings import T_ALPHABET
from core.settings import path_for_alphabetss
from tools.init_logging import init_logging
from tools.utils import _write_json_words_file, creat_file_name, _get_alphabets_from_txt_file_as_list

words_as_list = []


class FuzzGenerator:
    def __init__(self, alphabet: T_ALPHABET, words_count: int, word_length: int):
        self.alphabet = alphabet
        self.words_count = words_count
        self.word_length = word_length

    def create_the_first_words_of_the_alphabet(self) -> list:
        # there is a description of the work in README.md
        self.start_time = datetime.now()
        basic_symbols_of_alphabet_as_list = list(self.alphabet)
        logging.info(f'start - words: {len(words_as_list)}')
        for basic_symbol in basic_symbols_of_alphabet_as_list:
            if len(words_as_list) == self.words_count:
                break
            if len(basic_symbol) < self.word_length:
                for _ in range(self.word_length - 1):
                    basic_symbol += self.alphabet[0]
            elif self.word_length == 1:
                basic_symbol = basic_symbol
            words_as_list.append(basic_symbol[::-1])
        return words_as_list

    def create_the_rest_of_the_words(self, copy_word):
        list_in_process = []
        while_bool = True
        if copy_word != self.alphabet[0] * self.word_length:
            for symbol in self.alphabet:
                final_word = ''.join([copy_word, str(symbol)])
                final_word = final_word[len(final_word) - self.word_length:]
                if final_word in words_as_list or len(words_as_list) == self.words_count:
                    while_bool = False
                    break
                logging.info(f'word: "{final_word}" add to file')
                list_in_process.append(final_word)
        return list_in_process, while_bool

    #
    # words_as_list.append(final_word)

    def end_of_function(self) -> None:
        logging.info(f'end - words: {len(words_as_list)}')
        file_name = creat_file_name(self.alphabet, len(words_as_list), self.word_length)
        _write_json_words_file(file_name=file_name, words=words_as_list)
        logging.info(datetime.now() - self.start_time)


def main(*args):
    args = args[0]
    logging.info(args)
    fuzz_generator = FuzzGenerator(*args)
    words_as_list = fuzz_generator.create_the_first_words_of_the_alphabet()
    while_bool = True
    while while_bool:
        with concurrent.futures.ProcessPoolExecutor(max_workers=10) as executors:
            for list_in_process, while_bool_in_process in executors.map(fuzz_generator.create_the_rest_of_the_words,
                                                                        list(words_as_list)):
                while_bool = while_bool_in_process
                for word_in_process in list_in_process:
                    words_as_list.append(word_in_process)
    fuzz_generator.end_of_function()


if __name__ == '__main__':
    init_logging()
    alphabets_as_list = _get_alphabets_from_txt_file_as_list(path_for_alphabetss)
    with concurrent.futures.ProcessPoolExecutor(max_workers=len(alphabets_as_list)) as executor:
        executor.map(main, [(alphabet, 1000, 5) for alphabet in alphabets_as_list])
