from argparse import ArgumentParser, Namespace
from pathlib import PurePath

from .ls import pretty_print
from .daemon import mon

def _parse_args() -> Namespace:
    parser = ArgumentParser()
    subparsers = parser.add_subparsers(title="operation", required=True)

    _ = subparsers.add_parser("ls")

    daemon = subparsers.add_parser("daemon")
    daemon.add_argument("datasets", type=PurePath, nargs="+")

    return parser.parse_args()


def main() -> None:
    args = _parse_args()

    if args.operation == "ls":
        pretty_print()
    elif args.operation == "daemon":
        mon(args.datasets)
    else:
        assert False

