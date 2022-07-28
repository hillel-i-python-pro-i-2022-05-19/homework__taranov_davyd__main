import concurrent.futures
import logging

from fuzz_generator import FuzzGenerator
from settings import path_for_alfabets
from tools.init_logging import init_logging
from tools.tools import args, _get_alfabets_from_txt_file_as_list


def run(*args):
    args = args[0]
    logging.info(args)
    fuzz_generator = FuzzGenerator(*args)
    fuzz_generator.world_generator()


if __name__ == '__main__':
    arg = args()
    init_logging()
    alfabets_as_list = _get_alfabets_from_txt_file_as_list(path_for_alfabets)
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(alfabets_as_list)) as executor:
        executor.map(run, [(alfabet, arg.words_count, arg.word_length) for alfabet in alfabets_as_list])
