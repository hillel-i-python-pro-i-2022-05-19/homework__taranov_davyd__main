import logging

from fuzz_generator import FuzzGenerator
from tools.init_logging import init_logging
from tools.tools import args


def run(*args):
    args = args[0]
    logging.info(args)
    fuzz_generator = FuzzGenerator(*args)
    fuzz_generator.world_generator()
    fuzz_generator.start()


if __name__ == '__main__':
    arg = args()
    init_logging()
    run(arg.word_count, arg.word_length)
