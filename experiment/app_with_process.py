import concurrent.futures
import logging
from datetime import datetime
from multiprocessing import Pipe, Process

from core import *
from tools import _write_json_words_file, create_file_name, init_logging, _get_alphabets_from_txt_file_as_list


class FuzzGenerator:
    def __init__(self, alphabet: T_ALPHABET, words_count: int, word_length: int):
        self.alphabet = alphabet
        self.words_count = words_count
        self.word_length = word_length
        self.words_as_list = []
        self.increase_of_alphabet = -1
        self.input_data, self.output_data = Pipe()

    def creat_word(self, copy_word: str):
        words_as_list_in_proces = []
        if copy_word != self.alphabet[0] * self.word_length:
            for symbol in self.alphabet:
                final_word = ''.join([copy_word, str(symbol)])
                final_word = final_word[len(final_word) - self.word_length:]
                logging.info(f'word: "{final_word}" add to file')
                words_as_list_in_proces.append(final_word)
        self.output_data.send(words_as_list_in_proces)
        self.output_data.close()

    def word_generator(self) -> None:
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
        if len(self.alphabet) ** self.word_length < self.words_count:
            self.words_count = len(self.alphabet) ** self.word_length
        break_bool = True
        for copy_word in self.words_as_list:
            if not break_bool:
                break
            proces = Process(target=self.creat_word, args=(copy_word,))
            proces.start()
            for word in self.input_data.recv():
                if len(self.words_as_list) == self.words_count:
                    proces.join()
                    break_bool = False
                    break
                self.words_as_list.append(word)
                proces.join()

        logging.info(f'end - words: {len(self.words_as_list)}')
        logging.info(datetime.now() - start_time)
        file_name = create_file_name(self.alphabet, len(self.words_as_list), self.word_length)
        _write_json_words_file(file_name=file_name, words=self.words_as_list)


def main(*args):
    args = args[0]
    logging.info(args)
    fuzz_generator = FuzzGenerator(*args)
    fuzz_generator.word_generator()


if __name__ == '__main__':
    words_count = 100
    word_length = 5
    init_logging()
    alphabets_as_list = _get_alphabets_from_txt_file_as_list()
    with concurrent.futures.ProcessPoolExecutor() as executor:
        executor.map(main, [(alphabet, words_count, word_length) for alphabet in alphabets_as_list])
