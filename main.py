from fuzz_generator import FuzzGenerator, _write_json_words_file


def main(word_count, word_length):
    args = args()
    fuzz_generator = FuzzGenerator(word_count, word_length)
    words_list = fuzz_generator.world_generator()
    _write_json_words_file(path='words.json', words=words_list)
    fuzz_generator.start()


if __name__ == '__main__':
    main()
