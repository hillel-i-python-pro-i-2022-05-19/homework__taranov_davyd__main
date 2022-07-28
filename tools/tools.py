import argparse

def creat_file_name(url, len_urls: int, crawling_depth: int):
    file_name = url.split('https://')
    file_name = '|'.join(file_name[1].split('/'))
    file_name = f'''{file_name}(urls={len_urls})(depth={crawling_depth}).json'''

    return file_name

def args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-wc",
                        "--word_count",
                        type=int,
                        default=100,
                        help='Word count')
    parser.add_argument("-wl",
                        "--word_length",
                        type=int,
                        default=5,
                        help="World length")
    return parser.parse_args()
