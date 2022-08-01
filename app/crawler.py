import asyncio
import contextlib
import logging

import aiohttp
import bs4

from core.settings import T_URL, T_URLS, T_HTML_TEXTS
from tools.tools import creat_file_name, _added_urls_in_json_file


class Crawler:
    def __init__(self, input_url_as_str: T_URL, max_number_of_urls: int, crawling_depth: int):
        self.input_url_as_str = input_url_as_str
        self.urls_as_list: T_URLS = [input_url_as_str]
        self.max_number_of_urls = max_number_of_urls
        self.crawling_depth = crawling_depth

    async def get_text_from_url(self, html_text_as_list: T_HTML_TEXTS):
        index_for_while = -1
        logging.info(f'start, amount of html text: {len(html_text_as_list)}')
        with contextlib.suppress(TypeError):
            while True:
                await asyncio.sleep(0.003)
                if len(self.urls_as_list) == self.max_number_of_urls:
                    break
                index_for_while += 1
                async with aiohttp.ClientSession() as session:
                    try:
                        async with session.get(self.urls_as_list[index_for_while]) as response:
                            response_text = await response.text()
                            html_text_as_list.append(response_text)
                            logging.info(f'amount of html text: {len(html_text_as_list)}')
                    except IndexError:
                        index_for_while -= 1
                        continue
                    if index_for_while == self.crawling_depth - 1:
                        break
            logging.info(f'end, amount of html text: {len(html_text_as_list)}')

    async def get_urls_as_list(self, html_text_as_list: T_HTML_TEXTS):
        index_for_while = -1
        while_bool = True
        logging.info(f'start, amount of urls: {len(self.urls_as_list)}')
        while while_bool:
            await asyncio.sleep(0.003)
            index_for_while += 1
            try:
                soup = bs4.BeautifulSoup(markup=html_text_as_list[index_for_while], features='html.parser')
            except IndexError:
                index_for_while -= 1
                continue
            try:
                for url_element in soup.find_all('a'):
                    if len(self.urls_as_list) == self.max_number_of_urls:
                        while_bool = False
                    elif (('https' in url_element.get('href')[:5] or 'http' in url_element.get('href')[:4])) \
                            and url_element.get('href') not in self.urls_as_list \
                            and '.pdf' not in url_element.get('href')[-4:]:
                        self.urls_as_list.append(url_element.get('href'))
                        logging.info(f"New url: {url_element.get('href')}")
            except TypeError:
                continue
            if self.crawling_depth == len(html_text_as_list):
                break
        logging.info(f'end, amount of urls: {len(self.urls_as_list)}')

    async def main(self):
        html_text_as_list = []
        tasks = [
            Crawler.get_text_from_url(self, html_text_as_list),
            Crawler.get_urls_as_list(self, html_text_as_list)
        ]
        await asyncio.gather(*tasks)
        logging.info(f'end, urls={len(self.urls_as_list)}')
        file_name = creat_file_name(url=self.input_url_as_str,
                                    len_urls=len(self.urls_as_list),
                                    crawling_depth=self.crawling_depth)
        logging.info(f'File created: {file_name}')
        _added_urls_in_json_file(path=f'results/{file_name}', urls=self.urls_as_list)
