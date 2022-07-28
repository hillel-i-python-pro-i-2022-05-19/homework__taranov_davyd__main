import argparse
import json


def _get_alfabets_from_txt_file_as_list(path) -> T_ALFABETS:
    with open(path, "r", ) as file:
        data = ''
        for _ in file.readlines():
            data += _.split('\n')[0] + ','
    data = data[:-1]
    input_alfabets_as_list = data.split(",") if ',' in data else [data]
    return input_alfabets_as_list


def creat_file_name(alfabet, words_count, len_word: int):
    file_name = f'''{alfabet}(count={words_count})(len={len_word}).json'''
    return file_name


def _write_json_words_file(file_name, words: list):
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
