import argparse
import json
import logging
import threading

from settings import ALPHABET
from tools.init_logging import init_logging


def _write_json_words_file(path: str, words: list):
    with open(path, "w") as file:
        json.dump(words, file, indent=2)


class FuzzGenerator(threading.Thread):
    def __init__(self, word_count, word_length):
        threading.Thread.__init__(self)
        self.word_count = word_count
        self.word_length = word_length

    def world_generator(self) -> list:
        # there is a description of the work in README.md
        basic_symbols_of_alphabet_as_list = list(ALPHABET)
        # create a list of words from the characters of the entire alphabet
        words_list = []
        logging.info(f'start {len(words_list)}')
        increase_of_alphabet = -1
        for symbol in basic_symbols_of_alphabet_as_list:
            # fill words with the first character from the alphabet according to the length of the word
            if len(symbol) < self.word_length:
                for ___ in range(self.word_length - len(symbol)):
                    symbol += ALPHABET[0]
            elif self.word_length == 1:
                symbol = symbol
            words_list.append(symbol[::-1])
        if self.word_count <= len(words_list):
            words_list = words_list[:self.word_count]
            logging.info(f'end {len(words_list)}')
            return words_list
        while True:
            increase_of_alphabet += 1
            # depending on the number of words, increase the alphabet
            if len(ALPHABET) == len(words_list):
                copy_words_list = words_list.copy()
            else:
                copy_words_list = words_list.copy()[(len(ALPHABET)) * increase_of_alphabet:]
            # copy the list according to the length we need
            for index, __ in enumerate(copy_words_list):
                # create a new word in a double loop and add it to the list "words_list"
                if index == len(ALPHABET):
                    break
                if __ != ALPHABET[0] * self.word_length:
                    for _ in ALPHABET:
                        my_str = (__ + str(_))
                        my_str = my_str[len(my_str) - self.word_length:]
                        words_list.append(my_str)
            if len(words_list) >= self.word_count:
                # stop everything if we have created the required number of words
                break
        words_list = words_list[:self.word_count]
        logging.info(f'end {len(words_list)}')
        return words_list


def main(word_count, word_length, threads_count):
    for _ in range(int(threads_count)):
        fuzz_generator = FuzzGenerator(word_count, word_length)
        words_list = fuzz_generator.world_generator()
        _write_json_words_file(path='words.json', words=words_list)
        fuzz_generator.start()


parser = argparse.ArgumentParser()
parser.add_argument("action")
parser.add_argument("word_count", nargs='?', default=0)
parser.add_argument("word_length", nargs='?', default=0)
parser.add_argument("threads_count", nargs='?', default=0)
args = parser.parse_args()

try:
    if args.action == "GET_WORDS":
        init_logging()
        main(int(args.word_count), int(args.word_length), int(args.threads_count))
except ValueError:
    print('Что-то пошло не так :(')
