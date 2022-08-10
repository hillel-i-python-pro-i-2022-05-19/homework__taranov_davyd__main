import argparse
import json

from core.settings import T_ALPHABETS, T_FILE_NAME, T_JSON_FILE_NAME, T_ALPHABET, OUTPUT_PATH, INPUT_PATH


def _get_alphabets_from_txt_file_as_list() -> T_ALPHABETS:
    with open(INPUT_PATH, "r", ) as file:
        data = ''
        for readline in file.readlines():
            data += readline.split('\n')[0] + ','
    data = data[:-1]
    return data.split(",") if ',' in data else [data]


def create_file_name(alphabet: T_ALPHABET, words_count: int, word_len: int) -> T_FILE_NAME:
    return f'''{alphabet}(count={words_count})(word_len={word_len}).json'''


def _write_json_words_file(file_name: T_JSON_FILE_NAME, words: list) -> None:
    with open(OUTPUT_PATH.joinpath(file_name), "w") as file:
        json.dump(words, file, indent=2)



def args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-wc",
                        "--words_count",
                        type=int,
                        default=100,
                        help='Word count')
    parser.add_argument("-wl",
                        "--word_length",
                        type=int,
                        default=5,
                        help="Word length")
    return parser.parse_args()
