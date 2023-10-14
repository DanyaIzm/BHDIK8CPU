# height 11px
# width 11px
# side 5 px
# topleft 3 px

# start from y 3
# end with y 14
# start from x 3
# end with x 14

# set red color
data r3, 0xff
data r0, 0x6
outa r0
outd r3
data r1, 0x7
data r2, 0x8
data r3, 0x0
outa r1
outd r3
outa r2
outd r3

data r2, 14
data r0, 3
data r1, 3
rectangle:
    data r3, 0x4
    outa r3
    outd r0
    data r3, 0x5
    outa r3
    outd r1
    data r3, 0x9
    outa r3
    outd r3

    # increment x
    data r3, 1
    add r0, r3
    cmp r0, r2
    je inc_y

    jmp rectangle

    inc_y:
        add r1, r3
        data r0, 3
        cmp r2, r1
        ja rectangle
end_rectangle:

# set black color
data r3, 0
data r0, 0x6
outa r0
outd r3

# print left side
data r0, 3
data r3, 0x4
outa r3
outd r0
data r1, 4
data r2, 8
left_side:
    cmp r1, r2
    je end_left_side
    data r3, 0x5
    outa r3
    outd r1

    data r3, 1
    add r1, r3
    data r3, 0x9
    outa r3
    outd r3
    jmp left_side
end_left_side:


# print right side
data r0, 13
data r3, 0x4
outa r3
outd r0
data r1, 4
data r2, 8
right_side:
    cmp r1, r2
    je end_right_side
    data r3, 0x5
    outa r3
    outd r1

    data r3, 1
    add r1, r3
    data r3, 0x9
    outa r3
    outd r3
    jmp right_side
end_right_side:

# print top_left
data r0, 4
data r1, 3
data r3, 0x5
outa r3
outd r1
data r2, 7
top_left:
    cmp r0, r2
    je end_top_left
    data r3, 0x4
    outa r3
    outd r0

    data r3, 1
    add r0, r3
    data r3, 0x9
    outa r3
    outd r3
    jmp top_left
end_top_left:

# print top_right
data r0, 10
data r1, 3
data r3, 0x5
outa r3
outd r1
data r2, 13
top_right:
    cmp r0, r2
    je end_top_right
    data r3, 0x4
    outa r3
    outd r0

    data r3, 1
    add r0, r3
    data r3, 0x9
    outa r3
    outd r3
    jmp top_right
end_top_right:

# print bottom
data r2, 9
data r0, 4
data r1, 8

bottom_left:
    cmp r0, r2
    je end_bottom_left
    data r3, 0x4
    outa r3
    outd r0
    data r3, 0x5
    outa r3
    outd r1

    data r3, 1
    add r0, r3
    add r1, r3
    data r3, 0x9
    outa r3
    outd r3
    jmp bottom_left
end_bottom_left:

data r0, 9
data r1, 11
data r2, 13
bottom_right:
    cmp r0, r2
    je end_bottom_right
    data r3, 0x4
    outa r3
    outd r0
    data r3, 0x5
    outa r3
    outd r1

    # SUB 1's complement
    data r3, 1
    add r0, r3
    not r3, r3
    add r1, r3
    data r3, 1
    add r1, r3
    data r3, 0x9
    outa r3
    outd r3
    jmp bottom_right
end_bottom_right:

# print top hole
data r3, 0x9

data r0, 7
data r1, 4
data r2, 0x4
outa r2
outd r0
data r2, 0x5
outa r2
outd r1
outa r3
outd r3

data r0, 9
data r2, 0x4
outa r2
outd r0
outa r3
outd r3

data r0, 8
data r1, 5
data r2, 0x4
outa r2
outd r0
data r2, 0x5
outa r2
outd r1
outa r3
outd r3

hlt
