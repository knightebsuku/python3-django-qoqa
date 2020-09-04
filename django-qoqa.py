#!/usr/bin/python3

import argparse

from qoqa import qoqa
from colorama import init, Fore

init(autoreset=True)


def main():
    """
    Main Entry point for qoqa
    """
    parser = argparse.ArgumentParser(
        description="django-qoqa is an application to"
        " create a new django project and to"
        " build the django project and package it as a debian file."
    )
    subparsers = parser.add_subparsers(dest="commands")
    parser_new = subparsers.add_parser("new")
    parser_new.add_argument("name", help="name pf new django project")
    parser_new.add_argument("--template", help="path to template zip file")

    parser_build = subparsers.add_parser("build")
    parser_build.add_argument("--version", help="Version of this release")

    # parser_release = subparsers.add_parser("release")
    # parser_release.add_argument("--version", help="Version of this release")

    # parser_env = subparsers.add_parser("env")
    # parser_env.add_argument("name", help="name of virtual environment")
    # parser_env.add_argument("--version", help="Django version")

    args = parser.parse_args()
    if args.commands == "new":
        qoqa.create(args.name, args.template)
    elif args.commands == "build":
        qoqa.new_build(args.version)
    # elif args.commands == "release":
    #     qoqa.release(args.version)
    # elif args.action[0] == "env":
    #     qoqa.env(args.action[1])
    else:
        print(Fore.RED + "[qoqa] Unknown argument use either new, or build")
        exit()


if __name__ == "__main__":
    main()
