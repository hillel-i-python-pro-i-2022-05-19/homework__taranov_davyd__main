import argparse
import asyncio
import contextlib
import json
import logging
from contextvars import ContextVar
from typing import List, Dict, Union
from typing import TypeAlias

import aiohttp
import bs4

from init_logging import init_logging
from settings import path, url

T_URL: TypeAlias = str or list
T_URLS: TypeAlias = list[T_URL]
T_HTML_TEXT: TypeAlias = str

MyUrls = ContextVar('urls', default=[])


def _read_json_links_file(path: str) -> Union[List, Dict]:
    with open(path, 'r') as file:
        data = json.load(file)
    return data


def _write_json_links_file(path: str, urls: list, read_jason: list or dict):
    with open(path, "w") as file:
        read_jason.append(urls)
        json.dump(read_jason, file, indent=2)


async def get_text_from_url(url) -> T_HTML_TEXT:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            response_text = await response.text()
            return response_text


async def get_urls(text: T_HTML_TEXT, crawling_depth: int) -> T_URLS:
    soup = bs4.BeautifulSoup(markup=text, features='html.parser')
    urls = [link_element.get('href')
            for link_element in soup.find_all('a')
            if 'https' in link_element.get('href')[:5]][:crawling_depth]
    return urls


async def get_some_links(urls: T_URL, max_number_of_links: int, crawling_depth: int, ):
    new_urls = []
    if type(urls) == str:
        new_urls.append(urls)
    else:
        new_urls = urls
    logging.info(f'start {len(new_urls)}')
    while True:
        for index, _ in enumerate(new_urls):
            if index == max_number_of_links:
                break
            new_text = await get_text_from_url(_)
            with contextlib.suppress(TypeError):
                new_urls += await get_urls(new_text, crawling_depth)
        result = new_urls[:max_number_of_links]
        logging.info(f'end {len(result)}')
        return new_urls


async def main(max_number_of_links, crawling_depth):
    json_links_file_list = _read_json_links_file(path)
    tasks = [
        get_some_links(urls=url, max_number_of_links=max_number_of_links, crawling_depth=crawling_depth),
        get_some_links(urls=url, max_number_of_links=max_number_of_links, crawling_depth=crawling_depth),
    ]
    result = await asyncio.gather(*tasks)
    _write_json_links_file(path=path, urls=result[0], read_jason=json_links_file_list)


parser = argparse.ArgumentParser()
parser.add_argument("action")
parser.add_argument("max_number_of_links", nargs='?', default=0)
parser.add_argument("crawling_depth", nargs='?', default=0)
args = parser.parse_args()

try:
    if args.action == "GET_LINKS":
        init_logging()
        asyncio.run(main(int(args.max_number_of_links), int(args.crawling_depth)))
except ValueError:
    print('Something went wrong :(')
