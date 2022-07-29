import argparse
import json

from settings import T_ALFABETS, T_FILE_NAME, T_TXT_FILE_NAME, T_JSON_FILE_NAME, T_ALFABET


def _get_alfabets_from_txt_file_as_list(path: T_TXT_FILE_NAME) -> T_ALFABETS:
    with open(path, "r", ) as file:
        data = ''
        for _ in file.readlines():
            data += _.split('\n')[0] + ','
    data = data[:-1]
    return data.split(",") if ',' in data else [data]


def creat_file_name(alfabet: T_ALFABET, words_count: int, word_len: int) -> T_FILE_NAME:
    return f'''{alfabet}(count={words_count})(word_len={word_len}).json'''


def _write_json_words_file(file_name: T_JSON_FILE_NAME, words: list) -> None:
    with open(f'results/{file_name}', "w") as file:
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
                        help="World length")
    return parser.parse_args()
