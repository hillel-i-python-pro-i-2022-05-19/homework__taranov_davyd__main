import argparse


def args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--wc",
                        "-word_count",
                        type=int,
                        default=100)
    parser.add_argument("--wl"
                        "-word_length",
                        type=int,
                        default=5)
    return parser.parse_args()
