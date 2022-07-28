import logging

from settings import T_ALFABET
from tools.tools import _write_json_words_file, creat_file_name


class FuzzGenerator():
    def __init__(self, alfabet: T_ALFABET, words_count: int, word_length: int):
        self.alfabet = alfabet
        self.words_count = words_count
        self.word_length = word_length

    def world_generator(self) -> None:
        # there is a description of the work in README.md
        basic_symbols_of_alphabet_as_list = list(self.alfabet)
        # create a list of words from the characters of the entire alphabet
        words_as_list = []
        logging.info(f'start - words: {len(words_as_list)}')
        increase_of_alphabet = -1
        while_bool = True
        for basic_symbol in basic_symbols_of_alphabet_as_list:
            # fill words with the first character from the alphabet according to the length of the word
            if len(words_as_list) == self.words_count:
                break
            if len(basic_symbol) < self.word_length:
                for _ in range(self.word_length - len(basic_symbol)):
                    basic_symbol += self.alfabet[0]
            elif self.word_length == 1:
                basic_symbol = basic_symbol
            words_as_list.append(basic_symbol[::-1])
        if self.words_count <= len(words_as_list):
            words_as_list = words_as_list[:self.words_count]
            logging.info(f'end - words: {len(words_as_list)}')
            file_name = creat_file_name(self.alfabet, len(words_as_list), self.word_length)
            _write_json_words_file(file_name=file_name, words=words_as_list)
        while while_bool:
            increase_of_alphabet += 1
            # depending on the number of words, increase the alphabet
            if len(self.alfabet) == len(words_as_list):
                copy_words_list = words_as_list.copy()
            else:
                copy_words_list = words_as_list.copy()[(len(self.alfabet)) * increase_of_alphabet:]
            # copy the list of words of the length we need
            for copy_word in copy_words_list:
                # create a new word in a double loop and add it to the list "words_list"
                if copy_word != self.alfabet[0] * self.word_length:
                    for symbol in self.alfabet:
                        my_str = (copy_word + str(symbol))
                        my_str = my_str[len(my_str) - self.word_length:]
                        if my_str in words_as_list or len(words_as_list) >= self.words_count:
                            while_bool = False
                            break
                        logging.info(f'word: "{my_str}" add to file')
                        words_as_list.append(my_str)
        logging.info(f'end - words: {len(words_as_list)}')
        file_name = creat_file_name(self.alfabet, len(words_as_list), self.word_length)
        _write_json_words_file(file_name=file_name, words=words_as_list)
