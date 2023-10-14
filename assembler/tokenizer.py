from tokens import Token, TokenType
from instructions import INSTRUCTIONS


class TokenizeError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class Tokenizer:
    def __init__(self, strings: list[str]) -> None:
        self.strings = strings
        self.tokens = []

    def tokenize(self) -> list[Token]:
        try:
            return self._tokenize_unsafe()
        except TokenizeError as tokenize_error:
            raise tokenize_error
        except Exception as e:
            raise TokenizeError(f"File can't be parsed. Tokenizer catched an error {e}")

    def _tokenize_unsafe(self):
        for string in self.strings:
            if string.startswith("#"):
                # comment
                continue
            for str_part in string.split():
                if str_part.endswith(":"):
                    self.tokens.append(
                        Token(TokenType.LABEL, str_part.replace(":", ""))
                    )
                elif (
                    str_part.startswith("r")
                    and len(str_part) > 1
                    and str_part[1] in ["0", "1", "2", "3"]
                ):
                    self.tokens.append(
                        Token(TokenType.REGISTER, str_part.replace(",", ""))
                    )
                elif str_part in INSTRUCTIONS.keys():
                    self.tokens.append(Token(TokenType.INSTRUCTION, str_part))
                else:
                    try:
                        int(str_part)
                        self.tokens.append(Token(TokenType.IMMEDIATE, str_part))
                    except ValueError:
                        self.tokens.append(Token(TokenType.LABEL_REFERENCE, str_part))

        return self.tokens
