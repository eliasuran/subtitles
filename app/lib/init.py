import argparse

def parse_args() -> argparse.Namespace:
    '''
    should only return with .file
    '''
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--file', '-f', help='path to file')

    args = parser.parse_args()
    return args
