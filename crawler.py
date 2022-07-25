import asyncio
import contextlib
import logging

from settings import path_input_links
from tools.init_logging import init_logging
from tools.tools import _read_txt_file, _write_json_links_file, get_text_from_url, get_urls, creat_file_name, args


async def get_some_links(max_number_of_links: int, crawling_depth: int):
    input_links = _read_txt_file(path_input_links)
    given_urls_as_list = input_links.split(",") if ',' in input_links else [input_links]
    for url_from_list in given_urls_as_list:
        new_urls_as_list = [url_from_list]
        index_error_list = []
        index = -1
        logging.info(f'start {len(new_urls_as_list)}')
        while True:
            index += 1
            if crawling_depth == index or len(new_urls_as_list) >= max_number_of_links:
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
                new_urls_from_one_ulr = get_urls(new_text)
                for new_url in new_urls_from_one_ulr:
                    if new_url not in new_urls_as_list:
                        new_urls_as_list.append(new_url)
        result = new_urls_as_list[:max_number_of_links]
        logging.info(f'end {len(result)}')
        file_names = creat_file_name(url_from_list, len(result))
        _write_json_links_file(path=f'results/{file_names}', words=result)


async def main():
    arg = args()
    init_logging()
    tasks = [
        get_some_links(max_number_of_links=int(arg.max_number_of_links), crawling_depth=int(arg.crawling_depth))
    ]
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.run(main())
