first_program = [
    0b01000000,
    0b10101011,
    0b01101000,
]

second_program = [
    0b00100000,
    42,  # move value 42 to register R0
    0b00100001,
    15,  # move value 15 to register R1
    0b10000001,  # add R0 to R1 and get result in R0
    0b01101000,  # HLT
]

fibonacci = [
    0b00100000,
    1,  # 1 to R0
    0b00100001,
    1,  # 1 to R1
    0b10000001,  # R0 = R0 + R1
    0b10000100,  # R1 = R1 + R0
    0b01000000,
    4,
]

test_ld_sd = [
    0b00100000,
    42,  # 1 to R0
    0b00100001,
    15,  # 1 to R1
    0b00010001,  # store value at address R1 to R0
    0b00000101,  # load value at address R1 to R1
]

test_logic_arithmetic = [
    0b00100000,
    42,  # 1 to R0
    0b00100001,
    15,  # 1 to R1
    0b10000001,  # add R0 to R1, store in R0. Should be 0x39
    0b10010000,  # shr R0. Should be 0x1C
    0b10100000,  # shl R0. Should be 0x38
    0b10110001,  # not R0 and store in R1. Should be 0x38 R0 and 0xC7 R1
    0b11000001,  # And R0 and R1 and store in R0. Should be 0x00
    0b11110001,  # comapre R0 and R1
    0b00100000,
    42,  # 1 to R0
    0b11110001,  # comapre R0 and R1
    0b11100001,  # XOR R0 and R1 and store in R0. Should be 0xED
]


equal = [
    0b00100000,
    42,  # 42 to R0
    0b00100001,
    42,  # 42 to R1
    0b11110001,  # comapre R0 and R1. Should be equal
    0b00100000,
    88,  # 42 to R0
    0b11110001,  # comapre R0 and R1. R0 should be greater
    0b11110100,  # comapre R1 and R0. R1 should not be greater
]

clf = [
    0b00100000,
    42,  # 42 to R0
    0b00100001,
    42,  # 42 to R1
    0b11110001,  # comapre R0 and R1. Should be equal
    0b00110000,  # flags should be clear
]

jmpr = [0b00100000, 42, 0b00110000]  # 42 to R0  # jump to value in R0

nop = [
    0b00101111,
    0b00101111,
    0b00101111,
    0b00101111,
    0b00101111,
    0b00101111,
    0b00101111,
]

fibonacci_until_144 = [
    0b00100000,
    1,  # 1 to R0
    0b00100001,
    1,  # 1 to R1
    0b00100010,
    144,  # 144 to r2
    # loop (addr 6)
    0b10000001,  # R0 = R0 + R1
    0b11110010,  # cmp r0 and r2
    0b01010010,  # je end
    16,
    0b10000100,  # R1 = R1 + R0
    0b11110110,  # cmp R1 and r2
    0b01010010,  # je end
    16,
    0b01000000,  # jump loop
    6,
    # end (addr 16)
    0b01101000,  # hlt
]

conditional_jumps = [
    0b01010000,  # nojump
    0b01010001,  # should be z
    0b01010010,  # should be e
    0b01010100,  # should be a
    0b01011000,  # should be c
]

print_phrase_console = [
    0b00100000,
    0x1,  # address of a console to RA (addr 0x1)
    0b01111100,  # out address
    0b00100000,
    ord("H"),
    0b01111000,  # out letter H to console
    0b00100000,
    ord("e"),
    0b01111000,
    0b00100000,
    ord("l"),
    0b01111000,
    0b00100000,
    ord("l"),
    0b01111000,
    0b00100000,
    ord("o"),
    0b01111000,
    0b01101000,  # hlt
]

print_from_keyboard = [
    0b00100010,
    0x1,  # address of a console to R2 (addr 0x1)
    0b00100011,  # address of a keyboard to R3 (addr 0x3)
    0x3,
    0b00100001,  # 0 to r1
    0,
    # loop
    0b01111111,  # out address keyboard R3
    0b01110000,  # ind to R0
    0b11110001,  # cmp R0 to R1 (0)
    0b01010010,  # je loop
    6,
    0b01111110,  # out address console R2
    0b01111000,  # outd R0 to console
    0b01000000,  # jmp loop
    6,
]

# ONLY FOR 128x128 DISPLAY
# 0x4 - addrress of coord X
# 0x5 - addrress of coord Y
# 0x6 - addrress of color R
# 0x7 - addrress of color G
# 0x8 - addrress of color B
# 0x9 - addrress of screen write
# !LOOP! = 24
# INC_Y = 40
# PRINT = 48
# HLT = 54
write_line_on_screen_128 = [
    # set color #f77b4d to r1, r2 and r3
    0b00100001,
    0xF7,
    0b00100010,
    0x7B,
    0b00100011,
    0x4D,
    # set colors to monitor (addr to R0, ina, outd)
    # R
    0b00100000,
    0x6,
    0b01111100,
    0b01111001,
    # G
    0b00100000,
    0x7,
    0b01111100,
    0b01111010,
    # B
    0b00100000,
    0x8,
    0b01111100,
    0b01111011,
    # last column and row index to R3 to print a square
    0b00100011,
    73,
    # 53 to R1 (X pointer)
    0b00100001,
    53,
    # 53 to R2 (Y pointer)
    0b00100010,
    53,
    # !LOOP!
    # addr X to R0
    0b00100000,
    0x4,
    # outa of X
    0b01111100,
    # outd X
    0b01111001,
    # addr Y to R0
    0b00100000,
    0x5,
    # outa of Y
    0b01111100,
    # outd Y
    0b01111010,
    # increment X if X != 73 else increment Y
    # cmp R1, R3
    0b11110111,
    # je "INC_Y"
    0b01010010,
    40,
    # move 1 to R0
    0b00100000,
    1,
    # add R1 to R0
    0b10000100,
    # jmp PRINT
    0b01000000,
    48,
    # INC_Y
    # set X to initial value (53)
    # 53 to R1 (X pointer)
    0b00100001,
    53,
    # increment Y if Y != 73 else HLT
    # cmp R2, R3
    0b11111011,
    # je "HLT_L"
    0b01010010,
    54,
    # move 1 to R0
    0b00100000,
    1,
    # add R2 to R0
    0b10001000,
    # PRINT
    # move addr of screen to R0
    0b00100000,
    0x9,
    # outa of screen
    0b01111100,
    # out anything to screen to print
    0b01111000,
    # jmp !LOOP!
    0b01000000,
    24,
    # HLT
    0b01101000,
]

# ONLY FOR 32x32 DISPLAY
# 0x4 - addrress of coord X
# 0x5 - addrress of coord Y
# 0x6 - addrress of color R
# 0x7 - addrress of color G
# 0x8 - addrress of color B
# 0x9 - addrress of screen write
# !LOOP! = 24
# INC_Y = 40
# PRINT = 48
# HLT = 54
write_line_on_screen_32 = [
    # set color #f77b4d to r1, r2 and r3
    0b00100001,
    0xF7,
    0b00100010,
    0x7B,
    0b00100011,
    0x4D,
    # set colors to monitor (addr to R0, ina, outd)
    # R
    0b00100000,
    0x6,
    0b01111100,
    0b01111001,
    # G
    0b00100000,
    0x7,
    0b01111100,
    0b01111010,
    # B
    0b00100000,
    0x8,
    0b01111100,
    0b01111011,
    # last column and row index to R3 to print a square
    0b00100011,
    18,
    # 53 to R1 (X pointer)
    0b00100001,
    12,
    # 53 to R2 (Y pointer)
    0b00100010,
    12,
    # !LOOP!
    # addr X to R0
    0b00100000,
    0x4,
    # outa of X
    0b01111100,
    # outd X
    0b01111001,
    # addr Y to R0
    0b00100000,
    0x5,
    # outa of Y
    0b01111100,
    # outd Y
    0b01111010,
    # increment X if X != 73 else increment Y
    # cmp R1, R3
    0b11110111,
    # je "INC_Y"
    0b01010010,
    40,
    # move 1 to R0
    0b00100000,
    1,
    # add R1 to R0
    0b10000100,
    # jmp PRINT
    0b01000000,
    48,
    # INC_Y
    # set X to initial value (53)
    # 53 to R1 (X pointer)
    0b00100001,
    12,
    # increment Y if Y != 73 else HLT
    # cmp R2, R3
    0b11111011,
    # je "HLT_L"
    0b01010010,
    54,
    # move 1 to R0
    0b00100000,
    1,
    # add R2 to R0
    0b10001000,
    # PRINT
    # move addr of screen to R0
    0b00100000,
    0x9,
    # outa of screen
    0b01111100,
    # out anything to screen to print
    0b01111000,
    # jmp !LOOP!
    0b01000000,
    24,
    # HLT
    0b01101000,
]
# Really need an assembler. This is so painful to program such way

PROGRAMS_FOLDER = "./programs"

# change current program here
programs = [
    ("fibonacci_until_144", fibonacci_until_144),
    ("print_phrase_console", print_phrase_console),
    ("print_from_keyboard", print_from_keyboard),
    ("write_line_on_screen", write_line_on_screen_128),
    ("write_line_on_screen_32", write_line_on_screen_32),
]
programs = list(
    map(lambda x: (x[0], [y.to_bytes(1, "little") for y in x[1]]), programs)
)


for program in programs:
    with open(f"{PROGRAMS_FOLDER}/{program[0]}", "wb+") as file:
        for b in program[1]:
            file.write(b)
