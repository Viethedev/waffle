#!/usr/bin/env python
from __future__ import annotations

import argparse
import sys
import waffle

def format_number(x, *, threshold=1e6, sig=2):
    try:
        if abs(x) >= threshold:
            return f"{x:.{sig}e}"
        return f"{x:g}"
    except TypeError:
        return str(x)

class Console:
    def __init__(self) -> None:
        self.vm = waffle.WaffleStack()

    def run_file(self, path: str) -> None:
        bytecodes = self.vm.read(path)
        self.vm.execute(bytecodes)
        self.show_stack()

    def run_line(self, line: str) -> None:
        self.vm.interpret(line)
        self.show_stack()

    def show_stack(self) -> None:
        print("stack:", "".join([format_number(v) + " " for v in self.vm.datastack]))


def repl(console: Console) -> None:
    print("Waffle REPL")
    print("Type instructions, or 'leave' to leave")

    while True:
        try:
            line = input("waffle> ")
            if not line.strip():
                continue
            if line == "leave":
                break
            console.run_line(line)
        except KeyboardInterrupt:
            print("enter 'leave' to leave")
        except KeyError:
            print("Failed to load empty slot")

def main() -> None:
    parser = argparse.ArgumentParser(
        prog="waffle",
        description="Waffle VM command-line interface",
    )
    parser.add_argument(
        "file",
        nargs="?",
        help="Optional Waffle source file to run before entering REPL",
    )

    args = parser.parse_args()
    console = Console()

    if args.file:
        try:
            console.run_file(args.file)
        except Exception as exc:
            print("error:", exc)
            sys.exit(1)

    repl(console)


if __name__ == "__main__":
    main()
