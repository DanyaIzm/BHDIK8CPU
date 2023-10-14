## Instruction encoding in assembly and codes
|Code|Language|Mening|Added|
|---|---|---|---|
|1000RARB|ADD RA, RB|Add value in RA to the value in RB, store result in RA|YES|
|100100RA|SHR RA, RB|Shift value in RA one byte to the right|YES|
|101000RA|SHL RA, RB|Shift value in RA one byte to the left|YES|
|1011RARB|NOT RA, RB|NOT the value in the RA and put the result into RB|YES|
|1100RARB|AND RA, RB|AND RA with RB and put the result into RA|YES|
|1101RARB|OR RA, RB|OR RA with RB and put the result into RA|YES|
|1110RARB|XOR RA, RB|XOR RA with RB and put the result into RA|YES|
|1111RARB|CMP RA, RB|Compare RA with RB. Sets flags|YES|
|0000RARB|LD RA, RB|Load value from RAM at address in RB and store it in RA|YES|
|0001RARB|ST RA, RB|Store value from RA in RAM at address in RB|YES|
|001000RA|DATA RA, Imm|Load next value in RAM (Imm) to RA|YES|
|00101111|NOP|Do nothing|YES|
|001100RA|JMPR RA|Jump to address from RA|YES|
|01000000|JMP Imm|JMP to next value from RAM (Addr)|YES|
|0101CAEZ|JCAEZ Imm|JMP to next value from RAM (Addr) if any of flags CAEZ presented|YES|
|00110000|CLF|Clear FLAGS register|YES|
|01101000|HLT|Halt the CPU|YES|
|011100RA|IND RA|Input I/O data to register RA (Read data from selected I/O device)|YES|
|011101RA|INA RA|Input I/O address to register RA (Recieve an interrupt from I/O device)|YES|
|011110RA|OUTD RA|Ouput value in RA to I/O as data (Send data to selected I/O device)|YES|
|011111RA|OUTA RA|Output value in RA to I/O as address (select I/O device)|YES|
