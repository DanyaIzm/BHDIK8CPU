from tokens import Token, TokenType
from instructions import INSTRUCTIONS, IMMEDIATE_INSTRUCTIONS, JUMP_INSTRUCTIONS
from registers import REGISTERS


INSTRUCTION_LENGTH = 8


class ParserError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class Parser:
    def __init__(self, tokens: list[Token]) -> None:
        self.tokens = tokens
        self._labels: dict[str, int] = {}
        self._token_pointer = 0
        self._address_pointer = 0
        self._line_pointer = 1
        self._instructions: list[bytes | Token] = []

    def parse(self) -> list[bytes]:
        while self._token_pointer != len(self.tokens):
            token = self.tokens[self._token_pointer]

            match token.type:
                case TokenType.LABEL:
                    self._labels[token.content] = self._address_pointer
                    self._token_pointer += 1
                case TokenType.INSTRUCTION:
                    self._parse_instruction()
                case _:
                    raise ParserError(
                        "Can't parse file."
                        f"Invalid token type at line {self._line_pointer}:"
                        f"{token.type}. Expected LABEL or INSTRUCTION"
                    )

            self._line_pointer += 1

        self._resolve_label_references()
        return self._instructions

    def _parse_instruction(self) -> None:
        instruction = self.tokens[self._token_pointer]
        self._token_pointer += 1
        self._address_pointer += 1

        # get registers if needed
        instruction_bin = INSTRUCTIONS[instruction.content]

        if "RA" in instruction_bin:
            register = self._parse_register()
            instruction_bin = instruction_bin.replace("RA", register)
        if "RB" in instruction_bin:
            register = self._parse_register()
            instruction_bin = instruction_bin.replace("RB", register)

        self._instructions.append(int(instruction_bin, 2).to_bytes(1, "little"))
        if (
            instruction.content in JUMP_INSTRUCTIONS
            and self.tokens[self._token_pointer].type == TokenType.LABEL_REFERENCE
        ):
            self._parse_label_reference()
        elif instruction.content in IMMEDIATE_INSTRUCTIONS:
            self._parse_immediate()

    def _parse_label_reference(self):
        label_reference = self.tokens[self._token_pointer]
        self._token_pointer += 1
        self._address_pointer += 1

        if label_reference.type != TokenType.LABEL_REFERENCE:
            ParserError(
                "Can't parse file."
                f"Invalid token type at line {self._line_pointer}:"
                f"{label_reference.type}. Expected LABEL_REFERENCE"
            )

        self._instructions.append(label_reference)

    def _parse_immediate(self):
        immediate = self.tokens[self._token_pointer]
        self._token_pointer += 1
        self._address_pointer += 1

        if immediate.type != TokenType.LABEL_REFERENCE:
            ParserError(
                "Can't parse file."
                f"Invalid token type at line {self._line_pointer}:"
                f"{immediate.type}. Expected LABEL_REFERENCE"
            )

        base = (
            16
            if immediate.content.startswith("0x")
            else 2
            if immediate.content.startswith("0b")
            else 10
        )

        self._instructions.append(int(immediate.content, base).to_bytes(1, "little"))

    def _parse_register(self) -> str:
        register = self.tokens[self._token_pointer]
        self._token_pointer += 1

        if register.type != TokenType.REGISTER:
            raise ParserError(
                "Can't parse file. "
                f"Invalid token type at line {self._line_pointer}:"
                f"{register.type}. Expected REGISTER"
            )

        if register.content not in REGISTERS.keys():
            raise ParserError(
                "Can't parse file."
                f"Unknown register at line {self._line_pointer}: {register.content}"
            )

        return REGISTERS[register.content]

    def _resolve_label_references(self):
        for index, ref in enumerate(self._instructions):
            if isinstance(ref, Token):
                try:
                    self._instructions[index] = self._labels[ref.content].to_bytes(
                        1, "little"
                    )
                except KeyError:
                    raise ParserError(
                        "Can't parse file."
                        f"Can't resolve reference to label {ref.content}"
                    )
