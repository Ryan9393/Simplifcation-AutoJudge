import argparse
import asyncio

from judge.runner import run_leaderboard
from methods import METHODS
from sources import SOURCES


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run an AutoJudge leaderboard.")
    parser.add_argument("--source", choices=sorted(SOURCES), required=True)
    parser.add_argument("--method", choices=sorted(METHODS), required=True)
    parser.add_argument(
        "--k", type=int, default=None,
        help="Only score the first K requests (default: the full file).",
    )
    return parser.parse_args()


async def main() -> None:
    args = parse_args()
    source = SOURCES[args.source]
    method = METHODS[args.method]

    if method.REQUEST_KIND == "checklist_as_list" and source.checklist_as_list_path is None:
        raise SystemExit(f"Source '{args.source}' does not support method '{args.method}'.")

    output_path = await run_leaderboard(source, method, k=args.k)
    print(f"Wrote leaderboard to {output_path}")


if __name__ == "__main__":
    asyncio.run(main())
