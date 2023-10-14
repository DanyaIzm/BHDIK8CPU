data r0, 1
data r1, 1
data r2, 144

loop:   
    add r0, r1
    cmp r0, r2
    je end

    add r1, r0
    cmp r1, r2
    je end

    jmp loop

end:
    hlt
