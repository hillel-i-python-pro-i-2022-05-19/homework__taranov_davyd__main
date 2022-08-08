import concurrent.futures
import logging
import multiprocessing
from datetime import datetime

from core import *
from tools import init_logging, _get_alphabets_from_txt_file_as_list, create_file_name, \
    _write_json_words_file_for_experiment

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
                if final_word in words_as_list:
                    while_bool = False
                    return list_in_process, while_bool
                list_in_process.append(final_word)
        return list_in_process, while_bool

    def end_of_function(self) -> None:
        logging.info(f'end - words: {len(words_as_list)}')
        file_name = create_file_name(self.alphabet, len(words_as_list), self.word_length)
        _write_json_words_file_for_experiment(file_name=file_name, words=words_as_list)
        logging.info(datetime.now() - self.start_time)


def run(*args):
    args = args[0]
    logging.info(args)
    fuzz_generator = FuzzGenerator(*args)
    words_as_list = fuzz_generator.create_the_first_words_of_the_alphabet()
    while_bool = True
    index_3_a, index_2_a, index_1_a = -2, -2, -1
    index_3_b, index_2_b, index_1_b = -1, -1, 0
    if args[1] == 1:
        words_as_list = words_as_list[:1]
        while_bool = False
    while while_bool:
        index_1_a += 1
        index_1_b += 1
        if len(args[0]) == len(words_as_list):
            copy_words_list = words_as_list.copy()
        elif len(words_as_list) >= 1000:
            index_3_a += 1
            index_3_b += 1
            copy_words_list = words_as_list.copy()[1000 * index_3_a: 1000 * index_3_b]
        elif len(words_as_list) > 100:
            index_2_a += 1
            index_2_b += 1
            copy_words_list = words_as_list.copy()[100 * index_2_a: 100 * index_2_b]
        else:
            copy_words_list = words_as_list.copy()[10 * index_1_a: 10 * index_1_b]
        #  here I tried to somehow stop the process pool in the place I needed and at the same time speed it up
        with concurrent.futures.ProcessPoolExecutor(max_workers=10) as executors:
            for list_in_process, while_bool_in_process in executors.map(fuzz_generator.create_the_rest_of_the_words,
                                                                        list(copy_words_list)):
                while_bool = while_bool_in_process
                for word_in_process in list_in_process:
                    if len(words_as_list) == args[1]:
                        while_bool = False
                        break
                    words_as_list.append(word_in_process)
                    logging.info(f'word: "{word_in_process}" add to file')
    fuzz_generator.end_of_function()


if __name__ == '__main__':
    words_count = 10000
    word_length = 5
    init_logging()
    alphabets_as_list = _get_alphabets_from_txt_file_as_list(path_for_alphabets_for_experiment)
    with concurrent.futures.ProcessPoolExecutor(max_workers=multiprocessing.cpu_count() - 4) as executor:
        executor.map(run, [(alphabet, words_count, word_length) for alphabet in alphabets_as_list])
