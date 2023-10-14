class AssemblyWriter:
    def __init__(self, parsed_instructions: list[bytes]) -> None:
        self.parsed_instructions = parsed_instructions

    def write(self, file_path):
        with open(file_path, "wb") as file:
            for instruction in self.parsed_instructions:
                file.write(instruction)
