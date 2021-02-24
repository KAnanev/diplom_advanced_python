import os


def add_dir():
    if not os.path.exists('output_file'):
        os.mkdir('output_file')
