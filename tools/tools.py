import argparse
import json

from core.settings import T_URLS, T_FILE_NAME, T_JSON_FILE, T_URL, INPUT_PATH, OUTPUT_PATH


def _get_urls_from_txt_file_as_list() -> T_URLS:
    with open(INPUT_PATH, "r") as file:
        data = ''
        for _ in file.readlines():
            data += _.split('\n')[0] + ','
    data = data[:-1]
    input_urls_as_list = data.split(",") if ',' in data else [data]
    return input_urls_as_list



def _added_urls_in_json_file(path: T_JSON_FILE, urls: T_URLS) -> None:
    with open(f'{OUTPUT_PATH}/{path}', "w") as file:
        json.dump(urls, file, indent=2)


def creat_file_name(url: T_URL, len_urls: int, crawling_depth: int) -> T_FILE_NAME:
    file_name = url.split('https://')
    file_name = '|'.join(file_name[1].split('/'))
    file_name = f'''{file_name}(urls={len_urls})(depth={crawling_depth}).json'''
    return file_name


def args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-mn",
                        "--max_number_of_urls",
                        type=int,
                        default=100,
                        help='Required number of urls')
    parser.add_argument("-cd",
                        "--crawling_depth",
                        type=int,
                        default=300,
                        help='Crawling depth')
    return parser.parse_args()
