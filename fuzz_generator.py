import logging
import threading

from settings import ALPHABET
from tools.tools import _write_json_words_file, creat_file_name


class FuzzGenerator(threading.Thread):
    def __init__(self, alfabet, word_count, word_length):
        threading.Thread.__init__(self)
        self.alfabet = alfabet
        self.word_count = word_count
        self.word_length = word_length

    def world_generator(self) -> None:
        # there is a description of the work in README.md
        basic_symbols_of_alphabet_as_list = list(ALPHABET)
        # create a list of words from the characters of the entire alphabet
        words_list = []
        logging.info(f'start {len(words_list)}')
        increase_of_alphabet = -1
        while_bool = True
        for basic_symbol in basic_symbols_of_alphabet_as_list:
            # fill words with the first character from the alphabet according to the length of the word
            if len(basic_symbol) < self.word_length:
                for _ in range(self.word_length - len(basic_symbol)):
                    basic_symbol += ALPHABET[0]
            elif self.word_length == 1:
                basic_symbol = basic_symbol
            words_list.append(basic_symbol[::-1])
        if self.word_count <= len(words_list):
            words_list = words_list[:self.word_count]
            logging.info(f'end {len(words_list)}')
            _write_json_words_file(words=words_list)
        while while_bool:
            increase_of_alphabet += 1
            # depending on the number of words, increase the alphabet
            if len(ALPHABET) == len(words_list):
                copy_words_list = words_list.copy()
            else:
                copy_words_list = words_list.copy()[(len(ALPHABET)) * increase_of_alphabet:]
            # copy the list according to the length we need
            for index, copy_word in enumerate(copy_words_list):
                # create a new word in a double loop and add it to the list "words_list"
                if index == len(ALPHABET):
                    break
                if copy_word != ALPHABET[0] * self.word_length:
                    for symbol in ALPHABET:
                        my_str = (copy_word + str(symbol))
                        my_str = my_str[len(my_str) - self.word_length:]
                        if my_str in words_list:
                            while_bool = False
                            break
                        logging.info(f'word: {my_str} - add')
                        words_list.append(my_str)
            if len(words_list) >= self.word_count:
                # stop everything if we have created the required number of words
                break
        words_list = words_list[:self.word_count]
        logging.info(f'end {len(words_list)}')
        file_name = creat_file_name(self.alfabet, self.word_count, self.word_length)
        _write_json_words_file(file_name=file_name, words=words_list)
