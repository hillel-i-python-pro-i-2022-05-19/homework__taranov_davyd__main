import asyncio
import logging
import os
from multiprocessing import Pool

from crawler import Crawler
from settings import path_input_urls
from tools.init_logging import init_logging
from tools.tools import args, _get_urls_from_txt_file_as_list


def run(*args):
    args = args[0]
    logging.info(args)
    crawler = Crawler(*args)
    asyncio.run(crawler.get_unique_urls())


if __name__ == '__main__':
    print(os.listdir('results'))
    arg = args()
    init_logging()
    input_urls_as_list = _get_urls_from_txt_file_as_list(path_input_urls)
    with Pool(processes=len(input_urls_as_list)) as pool:
        pool.map(run,
                 [(input_url, arg.max_number_of_urls, arg.crawling_depth,) for input_url in input_urls_as_list])
