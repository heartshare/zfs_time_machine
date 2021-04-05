from argparse import ArgumentParser, Namespace

from .daemon import mon
from .ls import pretty_print


def _parse_args() -> Namespace:
    parser = ArgumentParser()
    subparsers = parser.add_subparsers(title="operation", required=True)

    _ = subparsers.add_parser("ls")

    _ = subparsers.add_parser("daemon")

    return parser.parse_args()


def main() -> None:
    args = _parse_args()

    if args.operation == "ls":
        pretty_print()
    elif args.operation == "daemon":
        mon()
    else:
        assert False
