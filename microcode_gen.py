from dataclasses import dataclass


RESCYCLE = 1 << 27
DA = 1 << 26
IO = 1 << 25
HLT = 1 << 24
IOCLKS = 1 << 23
SFLAGS = 1 << 22
SIR = 1 << 21
SIAR = 1 << 20
SR3 = 1 << 19
SR2 = 1 << 18
SR1 = 1 << 17
SR0 = 1 << 16
STMP = 1 << 15
SRAM = 1 << 14
SACC = 1 << 13
SMAR = 1 << 12
IOCLKE = 1 << 11
EBUS1 = 1 << 10
EIAR = 1 << 9
ER3 = 1 << 8
ER2 = 1 << 7
ER1 = 1 << 6
ER0 = 1 << 5
EACC = 1 << 4
ERAM = 1 << 3
ALU2 = 1 << 2
ALU1 = 1 << 1
ALU0 = 1 << 0


@dataclass
class Register:
    name: str
    address: str
    enable_signal: int
    set_signal: int


REGS = [
    Register("R0", "00", ER0, SR0),
    Register("R1", "01", ER1, SR1),
    Register("R2", "10", ER2, SR2),
    Register("R3", "11", ER3, SR3),
]


class Instruction:
    def __init__(self, address: int, microinstructions: list[int]) -> None:
        self.microinstructions = microinstructions
        if len(self.microinstructions) > 4:
            raise ValueError("Maximum allowed 7 steps for one instruction")

        self.address = address
        self.bytes: list[bytes] = self._get_instruction_bytes()

    def __str__(self) -> str:
        return f"{bin(self.address)}:{self.microinstructions}"

    def __repr__(self) -> str:
        return str(self)

    def _get_instruction_bytes(self) -> list[bytes]:
        instructions = [
            EIAR | EBUS1 | SMAR | SACC,
            ERAM | SIR,
            EACC | SIAR,
            *self.microinstructions,
        ]

        while len(instructions) != 8:
            instructions.append(RESCYCLE)

        instructions = list(map(lambda x: x.to_bytes(4, "little"), instructions))

        return instructions


class ConditionalJumpInstruction(Instruction):
    def __init__(
        self, address: int, microinstructions: list[int], mask: int = 0b0000
    ) -> None:
        self.mask = mask
        super().__init__(address | mask, microinstructions)


class RegisterInstructions:
    def __init__(
        self, address_blueprint: str, microinstructions: list[tuple[str, int]]
    ) -> None:
        blueprints = []

        # replace RA register
        if "RA" in address_blueprint:
            for reg in REGS:
                address = address_blueprint.replace("RA", str(reg.address))
                instructions = []
                for bp_ins in microinstructions:
                    if "RA" not in bp_ins[0]:
                        instructions.append(bp_ins)
                        continue

                    if "RA[E]" in bp_ins:
                        instructions.append(
                            (
                                bp_ins[0].replace("RA[E]", ""),
                                reg.enable_signal | bp_ins[1],
                            )
                        )
                    else:  # "RA[S]"
                        instructions.append(
                            (bp_ins[0].replace("RA[S]", ""), reg.set_signal | bp_ins[1])
                        )
                blueprints.append([address, instructions])

        # replace RB register
        if "RB" in address_blueprint:
            new_blueprints = []
            for bp in blueprints:
                for reg in REGS:
                    address = bp[0].replace("RB", str(reg.address))
                    instructions = []
                    for bp_ins in bp[1]:
                        if "RB" not in bp_ins[0]:
                            instructions.append(bp_ins)
                            continue

                        if "RB[E]" in bp_ins:
                            instructions.append(
                                (
                                    bp_ins[0].replace("RB[E]", ""),
                                    reg.enable_signal | bp_ins[1],
                                )
                            )
                        else:  # "RB[S]"
                            instructions.append(
                                (
                                    bp_ins[0].replace("RB[S]", ""),
                                    reg.set_signal | bp_ins[1],
                                )
                            )
                    new_blueprints.append([address, instructions])

            blueprints = new_blueprints

        self.instructions = [
            Instruction(
                int(bp[0].replace("0b", ""), base=2),
                [int(i[1]) for i in bp[1]],
            )
            for bp in blueprints
        ]


class InstructionCollection:
    def __init__(
        self,
        instructions: list[
            Instruction | RegisterInstructions | ConditionalJumpInstruction
        ],
    ) -> None:
        self.instructions = {}
        self._convert_instructions(instructions)

    def __contains__(self, key) -> bool:
        if key in self.instructions.keys():
            return True

        return False

    def __getitem__(
        self, key
    ) -> Instruction | RegisterInstructions | ConditionalJumpInstruction:
        return self.instructions[key]

    def _convert_instructions(
        self,
        instructions: list[
            Instruction | RegisterInstructions | ConditionalJumpInstruction
        ],
    ) -> None:
        for instruction in instructions:
            if isinstance(instruction, Instruction):
                self.instructions[instruction.address] = instruction
            elif isinstance(instruction, RegisterInstructions):
                for ins in instruction.instructions:
                    self.instructions[ins.address] = ins


nop = Instruction(0b00101111, [])
halt = Instruction(0b01101000, [HLT])
jmp = Instruction(0b01000000, [EIAR | SMAR, ERAM | SIAR])
clf = Instruction(0b00110000, [EBUS1 | SFLAGS])
data = RegisterInstructions(
    "0b001000RA",
    [
        ("", EIAR | SMAR),
        ("RA[S]", ERAM),
        ("", EBUS1 | EIAR | SACC),
        ("", EACC | SIAR),
    ],
)
jmpr = RegisterInstructions("0b001100RA", [("RA[E]", EIAR)])
add = RegisterInstructions(
    "0b1000RARB",
    [
        ("RA[E]", STMP),
        ("RB[E]", SACC | SFLAGS),
        ("RA[S]", EACC),
    ],
)
not_ins = RegisterInstructions(
    "0b1011RARB",
    [("RA[E]", ALU0 | ALU1 | SACC | SFLAGS), ("RB[S]", EACC)],
)
shl = RegisterInstructions(
    "0b101000RA",
    [
        ("RA[E]", ALU1 | SACC | SFLAGS),
        ("RA[S]", EACC),
    ],
)
shr = RegisterInstructions(
    "0b100100RA",
    [
        ("RA[E]", ALU0 | SACC | SFLAGS),
        ("RA[S]", EACC),
    ],
)
and_ins = RegisterInstructions(
    "0b1100RARB",
    [
        ("RA[E]", STMP),
        ("RB[E]", ALU2 | SACC | SFLAGS),
        ("RA[S]", EACC),
    ],
)
or_ins = RegisterInstructions(
    "0b1101RARB",
    [
        ("RA[E]", STMP),
        ("RB[E]", ALU2 | ALU0 | SACC | SFLAGS),
        ("RA[S]", EACC),
    ],
)
xor = RegisterInstructions(
    "0b1110RARB",
    [
        ("RA[E]", STMP),
        ("RB[E]", ALU2 | ALU1 | SACC | SFLAGS),
        ("RA[S]", EACC),
    ],
)
cmp = RegisterInstructions(
    "0b1111RARB",
    [
        ("RB[E]", STMP),
        ("RA[E]", ALU2 | ALU1 | ALU0 | SFLAGS),
    ],
)
ld = RegisterInstructions("0b0000RARB", [("RB[E]", SMAR), ("RA[S]", ERAM)])
sd = RegisterInstructions("0b0001RARB", [("RB[E]", SMAR), ("RA[E]", SRAM)])
ind = RegisterInstructions(
    "0b011100RA",
    [
        ("RA[S]", IOCLKE),
    ],
)
ina = RegisterInstructions(
    "0b011101RA",
    [
        ("RA[S]", DA | IOCLKE),
    ],
)
outd = RegisterInstructions(
    "0b011110RA",
    [
        ("RA[E]", IO | IOCLKS),
    ],
)
outa = RegisterInstructions(
    "0b011111RA",
    [
        ("RA[E]", DA | IO | IOCLKS),
    ],
)

# conditional jumps 0101CAEZ
nojump = ConditionalJumpInstruction(
    0b01010000,
    # increment IAR
    [EIAR | EBUS1 | SACC, EACC | SIAR],
    mask=0b0000,
)
jc = ConditionalJumpInstruction(0b01010000, jmp.microinstructions, mask=0b1000)
ja = ConditionalJumpInstruction(0b01010000, jmp.microinstructions, mask=0b0100)
je = ConditionalJumpInstruction(0b01010000, jmp.microinstructions, mask=0b0010)
jz = ConditionalJumpInstruction(0b01010000, jmp.microinstructions, mask=0b0001)
jca = ConditionalJumpInstruction(0b01010000, jmp.microinstructions, mask=0b1100)
jce = ConditionalJumpInstruction(0b01010000, jmp.microinstructions, mask=0b1010)
jcz = ConditionalJumpInstruction(0b01010000, jmp.microinstructions, mask=0b1001)
jae = ConditionalJumpInstruction(0b01010000, jmp.microinstructions, mask=0b0110)
jaz = ConditionalJumpInstruction(0b01010000, jmp.microinstructions, mask=0b0101)
jez = ConditionalJumpInstruction(0b01010000, jmp.microinstructions, mask=0b0011)
jcae = ConditionalJumpInstruction(0b01010000, jmp.microinstructions, mask=0b1110)
jcaz = ConditionalJumpInstruction(0b01010000, jmp.microinstructions, mask=0b1101)
jcez = ConditionalJumpInstruction(0b01010000, jmp.microinstructions, mask=0b1011)
jaez = ConditionalJumpInstruction(0b01010000, jmp.microinstructions, mask=0b0111)
jcaez = ConditionalJumpInstruction(0b01010000, jmp.microinstructions, mask=0b1111)

instruction_collection = InstructionCollection(
    [
        nop,
        halt,
        jmp,
        jmpr,
        data,
        add,
        not_ins,
        shl,
        shr,
        and_ins,
        or_ins,
        xor,
        cmp,
        ld,
        sd,
        clf,
        ind,
        ina,
        outd,
        outa,
    ]
)
conditional_jumps_collection = InstructionCollection(
    [
        # conditional jumps
        nojump,
        jc,
        ja,
        je,
        jz,
        jca,
        jce,
        jcz,
        jae,
        jaz,
        jez,
        jcae,
        jcaz,
        jcez,
        jaez,
        jcaez,
    ]
)


STEP_FLAGS_BITS_AMOUNT = 8
STEP_BITS_AMOUNT = 3
INSTRUCTION_FULL_LENGTH = 1 << STEP_FLAGS_BITS_AMOUNT
INSTRUCTION_STEP_PART_LENGTH = 1 << STEP_BITS_AMOUNT

with open("microcode.bin", "wb") as file:
    for addr in range(0x100):
        # if conditional jump
        if addr in conditional_jumps_collection:
            instruction = conditional_jumps_collection[addr]
            for mask_addr in range(
                0,
                INSTRUCTION_FULL_LENGTH,
                INSTRUCTION_STEP_PART_LENGTH,
            ):
                if mask_addr == (instruction.mask << STEP_BITS_AMOUNT):
                    for word in instruction.bytes:
                        file.write(word)
                else:
                    for word in nojump.bytes:
                        file.write(word)
            continue

        if addr in instruction_collection:
            instruction_b = instruction_collection[addr].bytes
        else:
            instruction_b = nop.bytes

        for _ in range(INSTRUCTION_FULL_LENGTH // 8):
            for word in instruction_b:
                file.write(word)
