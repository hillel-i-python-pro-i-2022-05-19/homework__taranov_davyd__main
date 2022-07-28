import argparse


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


def awdawd():
    parser = argparse.ArgumentParser()
    parser.add_argument("-mn",
                        "--max_number_of_urls",
                        type=int,
                        default=100,
                        help='Required number of urls')
    parser.add_argument("-cd",
                        "--crawling_depth",
                        type=int,
                        default=100,
                        help='Crawling depth')
    return parser.parse_args()
