import argparse
import json

import aiohttp
import bs4

from settings import T_HTML_TEXT, T_URLS, T_FILE_NAME, T_JSON_FILE, T_TXT_FILE, T_URL


def _get_urls_from_txt_file_as_list(path: T_TXT_FILE) -> T_URLS:
    with open(path, "r", ) as file:
        data = ''
        for _ in file.readlines():
            data += _.split('\n')[0] + ','
    data = data[:-1]
    input_urls_as_list = data.split(",") if ',' in data else [data]
    return input_urls_as_list


def _added_urls_in_json_file(path: T_JSON_FILE, urls: T_URLS) -> None:
    with open(path, "w") as file:
        json.dump(urls, file, indent=2)


async def get_text_from_url(url: T_URL) -> T_HTML_TEXT:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            response_text = await response.text()
            return response_text


def get_urls(text: T_HTML_TEXT) -> T_URLS:
    soup = bs4.BeautifulSoup(markup=text, features='html.parser')
    urls = [url_element.get('href')
            for url_element in soup.find_all('a')
            if 'https' or 'http' in url_element.get('href')[:5]]
    return urls


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
                        default=100,
                        help='Crawling depth')
    return parser.parse_args()
