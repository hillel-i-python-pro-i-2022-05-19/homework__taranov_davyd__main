import contextlib
import logging
import time

from settings import T_URL
from tools.tools import _added_urls_in_json_file, get_text_from_url, get_urls_as_list, creat_file_name


class Crawler:
    def __init__(self, input_url_as_str: T_URL, max_number_of_urls: int, crawling_depth: int):
        self.input_url_as_str = input_url_as_str
        self.max_number_of_urls = max_number_of_urls
        self.crawling_depth = crawling_depth

    async def get_unique_urls(self) -> None:
        new_urls_as_list = [self.input_url_as_str]
        index = -1
        logging.info(f'start, urls={len(new_urls_as_list)}')
        while_bool = True
        while while_bool:
            index += 1
            if self.crawling_depth == index:
                break
            new_text = await get_text_from_url(new_urls_as_list[index])
            with contextlib.suppress(TypeError):
                new_urls_from_one_ulr = get_urls_as_list(new_text)
                for new_url in new_urls_from_one_ulr:
                    if len(new_urls_as_list) == self.max_number_of_urls:
                        while_bool = False
                        break
                    if new_url not in new_urls_as_list:
                        new_urls_as_list.append(new_url)
                        logging.info(f'New url: {new_url}')
                        time.sleep(0.03)
        logging.info(f'end, urls={len(new_urls_as_list)}')
        file_name = creat_file_name(url=self.input_url_as_str,
                                    len_urls=len(new_urls_as_list),
                                    crawling_depth=self.crawling_depth)
        logging.info(f'File created: {file_name}')
        _added_urls_in_json_file(path=f'results/{file_name}', urls=new_urls_as_list)
