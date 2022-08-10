import asyncio
import logging
from multiprocessing import Pool

from app.crawler import Crawler
from tools.init_logging import init_logging
from tools.tools import args, _get_urls_from_txt_file_as_list


def run(*args):
    args = args[0]
    logging.info(args)
    crawler = Crawler(*args)
    asyncio.run(crawler.main())


if __name__ == '__main__':
    arg = args()
    init_logging()
    input_urls_as_list = _get_urls_from_txt_file_as_list()
    print(input_urls_as_list)
    with Pool(processes=len(input_urls_as_list)) as pool:
        pool.map(run,
                 [(input_url, arg.max_number_of_urls, arg.crawling_depth) for input_url in input_urls_as_list])
