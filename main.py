import concurrent.futures
import logging

from app.fuzz_generator import FuzzGenerator
from core.settings import path_for_alphabets
from tools.init_logging import init_logging
from tools.utils import args, _get_alphabets_from_txt_file_as_list


def run(*args):
    args = args[0]
    logging.info(args)
    fuzz_generator = FuzzGenerator(*args)
    fuzz_generator.words_generator()

if __name__ == '__main__':
    arg = args()
    init_logging()
    alphabets_as_list = _get_alphabets_from_txt_file_as_list(path_for_alphabets)
    with concurrent.futures.ProcessPoolExecutor(max_workers=len(alphabets_as_list)) as executor:
        executor.map(run, [(alphabet, arg.words_count, arg.word_length) for alphabet in alphabets_as_list])
