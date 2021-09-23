import argparse


def string_length(string):
    count = 0
    for char in string:
        count += 1
    print(count)
    return count


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Character Counter')
    parser.add_argument('--string', action='store', type=str)
    results = parser.parse_args()
    string = results.string

    string_length(string)
