import argparse
import asyncio
import json
import logging
from typing import List, Dict, Union

from init_logging import init_logging
from settings import ALPHABET, path_for_words


def _read_json_words_file(path: str) -> Union[List, Dict]:
    with open(path, 'r') as file:
        data = json.load(file)
    return data


def _write_json_words_file(path: str, words: list, read_json: list or dict):
    with open(path, "w") as file:
        read_json += list(words)
        json.dump(read_json, file, indent=2)


async def fuzz_generator(word_count: int, word_length: int) -> list:
    # there is a description of the work in README.md
    basic_symbols_of_alphabet_as_list = list(ALPHABET)
    # create a list of words from the characters of the entire alphabet
    words_list = []
    logging.info(f'start {len(words_list)}')
    increase_of_alphabet = -1
    for symbol in basic_symbols_of_alphabet_as_list:
        # fill words with the first character from the alphabet according to the length of the word
        if len(symbol) < word_length:
            for ___ in range(word_length - len(symbol)):
                symbol += ALPHABET[0]
            words_list.append(symbol[::-1])
    if word_count <= len(words_list):
        words_list = words_list[:word_count]
        logging.info(f'end {len(words_list)}')
        return words_list
    while True:
        increase_of_alphabet += 1
        # depending on the number of words, increase the alphabet
        if len(ALPHABET) == len(words_list):
            copy_words_list = words_list.copy()
        else:
            copy_words_list = await words_list.copy()[(len(ALPHABET)) * increase_of_alphabet:]
        # copy the list according to the length we need
        for index, __ in enumerate(copy_words_list):
            # create a new word in a double loop and add it to the list "words_list"
            if index == len(ALPHABET):
                break
            if __ != ALPHABET[0] * word_length:
                for _ in ALPHABET:
                    my_str = await (__ + str(_))
                    my_str = my_str[len(my_str) - word_length:]
                    words_list.append(my_str)
        if len(words_list) >= word_count:
            # stop everything if we have created the required number of words
            break
    words_list = words_list[:word_count]
    logging.info(f'end {len(words_list)}')
    return words_list


async def main(first_arg: int, second_arg: int):
    json_words_file_as_list = _read_json_words_file(path=path_for_words)
    words = await fuzz_generator(first_arg, second_arg)
    _write_json_words_file(path=path_for_words, words=words, read_json=json_words_file_as_list)


parser = argparse.ArgumentParser()
parser.add_argument("action")
parser.add_argument("first_arg", nargs='?', default=0)
parser.add_argument("second_arg", nargs='?', default=0)
args = parser.parse_args()

try:
    if args.action == "GET_WORDS":
        init_logging()
        asyncio.run(main(int(args.first_arg),
                         int(args.second_arg)))
except ValueError:
    print('Что-то пошло не так :(')
