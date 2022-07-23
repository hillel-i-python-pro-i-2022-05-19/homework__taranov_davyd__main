import argparse
import asyncio
import contextlib
import json
import logging
from typing import List, Dict, Union, TypeAlias

import aiohttp
import bs4

from init_logging import init_logging
from settings import path_for_links, url

T_URL: TypeAlias = str
T_URLS: TypeAlias = list[T_URL]
T_HTML_TEXT: TypeAlias = str


def _read_json_links_file(path: str) -> Union[List, Dict]:
    with open(path, 'r') as file:
        data = json.load(file)
    return data


def _write_json_links_file(path: str, urls: list, read_json: list or dict):
    with open(path, "w") as file:
        read_json += list(urls)
        json.dump(read_json, file, indent=2)


async def get_text_from_url(url) -> T_HTML_TEXT:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            response_text = await response.text()
            return response_text


async def get_urls(text: T_HTML_TEXT, crawling_depth: int) -> T_URLS:
    soup = bs4.BeautifulSoup(markup=text, features='html.parser')
    urls = [link_element.get('href')
            for link_element in soup.find_all('a')[:crawling_depth - 1]
            if 'https' in link_element.get('href')[:5]]
    return urls


async def get_some_links(url: T_URL, max_number_of_links: int, crawling_depth: int) -> list:
    new_urls_as_list = [url]
    index_error_list = []
    index = -1
    logging.info(f'start {len(new_urls_as_list)}')
    while True:
        index += 1
        if len(new_urls_as_list) >= max_number_of_links:
            break
        try:
            new_text = await get_text_from_url(new_urls_as_list[index])
        except IndexError:
            index_error = "Недостаточно глубины:("
            index_error_list.append(index_error)
            print(index_error)
            index += -1
            if len(index_error_list) > 5:
                print('ооо, нет, Мы зациклились... :*(')
                break
            continue
        with contextlib.suppress(TypeError):
            new_urls_from_one_ulr = await get_urls(new_text, crawling_depth)
            for _ in new_urls_from_one_ulr:
                if _ not in new_urls_as_list:
                    new_urls_as_list.append(_)
    result = new_urls_as_list[:max_number_of_links]
    logging.info(f'end {len(result)}')
    return result


async def main(first_arg, second_arg):
    json_links_file_list = _read_json_links_file(path_for_links)
    tasks = [
        get_some_links(url=url,
                       max_number_of_links=first_arg,
                       crawling_depth=second_arg)
    ]
    result = await asyncio.gather(*tasks)
    _write_json_links_file(path=path_for_links,
                           urls=result[0],
                           read_json=json_links_file_list)


parser = argparse.ArgumentParser()
parser.add_argument("action")
parser.add_argument("first_arg", nargs='?', default=0)
parser.add_argument("second_arg", nargs='?', default=0)
args = parser.parse_args()

try:
    if args.action == "GET_LINKS":
        init_logging()
        asyncio.run(main(int(args.first_arg),
                         int(args.second_arg)))
except ValueError:
    print('Что-то пошло не так :(')
