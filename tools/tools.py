import argparse
import json

import aiohttp
import bs4

from settings import T_HTML_TEXT, T_URLS


def _read_txt_file(path: str) -> str:
    with open(path, "r", ) as file:
        data = ''
        for _ in file.readlines():
            data += _.split('\n')[0] + ','
    return data[:-1]


def _write_json_links_file(path: str, words: list):
    with open(path, "w", ) as file:
        json.dump(words, file, indent=2)


async def get_text_from_url(url) -> T_HTML_TEXT:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            response_text = await response.text()
            return response_text


def get_urls(text: T_HTML_TEXT) -> T_URLS:
    soup = bs4.BeautifulSoup(markup=text, features='html.parser')
    urls = [link_element.get('href')
            for link_element in soup.find_all('a')
            if 'https' in link_element.get('href')[:5]]
    return urls


def creat_file_name(url: str, len_urls: int) -> str:
    names_the_start = url.split('https://')
    names_the_end = f'''{names_the_start[1].split('/')[0]}({len_urls}).json'''
    return names_the_end


def args():
    parser = argparse.ArgumentParser(description='Say hello')
    parser.add_argument("max_number_of_links", nargs='?', default=0, help='Required number of links')
    parser.add_argument("crawling_depth", nargs='?', default=0, help='crawling_depth')
    return parser.parse_args()
