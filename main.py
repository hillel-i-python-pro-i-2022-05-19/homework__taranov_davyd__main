from fuzz_generator import FuzzGenerator, _write_json_words_file


def run(*args):
    arg = args()
    fuzz_generator = FuzzGenerator()
    words_list = fuzz_generator.world_generator()
    _write_json_words_file(path='words.json', words=words_list)
    fuzz_generator.start()


if __name__ == '__main__':
    run()
