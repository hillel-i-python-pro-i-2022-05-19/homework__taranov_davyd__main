import argparse
import json


def _get_urls_from_txt_file_as_list(path):
    with open(path, "r", ) as file:
        data = ''
        for _ in file.readlines():
            data += _.split('\n')[0] + ','
    data = data[:-1]
    input_urls_as_list = data.split(",") if ',' in data else [data]
    return input_urls_as_list


def creat_file_name(alfabet, count_word, len_word: int):
    file_name = f'''{alfabet}(count={count_word})(len={len_word}).json'''
    return file_name


def _write_json_words_file(file_name, words: list):
    with open(file_name, "w") as file:
        json.dump(words, file, indent=2)


def args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-wc",
                        "--word_count",
                        type=int,
                        default=100,
                        help='Word count')
    parser.add_argument("-wl",
                        "--word_length",
                        type=int,
                        default=5,
                        help="World length")
    return parser.parse_args()
