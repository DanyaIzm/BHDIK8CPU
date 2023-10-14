import sys

from tokenizer import Tokenizer
from parser import Parser
from writer import AssemblyWriter


def main():
    if len(sys.argv) != 3:
        print("Usage: python assembler.py <source> <output>")
        print("Options:")
        print("<source> - file written in BHDIK8 assembly")
        print("<output> - compiled binary program for BHDIK8 CPU")

        return 1

    with open(sys.argv[1], "r") as assembly_file:
        file_contains = assembly_file.readlines()

    strings = list(
        filter(
            lambda x: x,
            map(
                lambda x: x.replace("\n", "").replace("\t", "").strip(),
                file_contains,
            ),
        )
    )

    tokens = Tokenizer(strings).tokenize()

    parsed_content = Parser(tokens).parse()

    AssemblyWriter(parsed_content).write(sys.argv[2])


if __name__ == "__main__":
    main()
