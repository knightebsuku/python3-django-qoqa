#!/usr/bin/python3

import argparse

from qoqa import qoqa


def main():
    """
    Main Entry point for qoqa
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--new',
                        help='Create new django project')
    parser.add_argument('-b', '--build-project',
                        help='Build django project')

    args = parser.parse_args()
    if args.new:
        print("Starting new django project")
    qoqa.project()


if __name__ == '__main__':
    main()
