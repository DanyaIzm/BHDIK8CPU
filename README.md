# 8-bit microcoded CPU

8-битный процессор, управляемый микрокодом.

Генератор микрокода и ассемблер написаны на Python.

---

**Ахитектура команд (ISA) описана в файле [ISA.md](./ISA.md)**

**Файлы:**
1. BHDIK8.circ - файл схемы процессора для Logisim Evolution;
2. [microcode_gen.py](./microcode_gen.py) - генератор микрокода. Записывает микрокод (65 536 (2^16) 32-битных инструкций) в файл microcode.bin;
3. [microasm.py](./microasm.py) - микроассемблер, который по шестнадцатиричным/двоичным кодам собирает программу в бинарный файл;
4. [assembler/assembler.py](./assembler/assembler.py) - главный файл модуля полноценного ассеблера, поддерживающего весь ISA BHDIK8 и создание лэйблов для прыжков;
5. [assembly_progs/*](./assembly_progs) - простенькие программы, написанные на ассемблере под BHDIK8;
6. [compiled_programs/*](./compiled_programs) - сассемблированные программы с помощью микроассемблера и ассемблера.

---

**Ссылки:**
- [Официальный сайт книги "But How to It Know?"](http://www.buthowdoitknow.com/)
- [YouTube плейтист по данной книге](https://www.youtube.com/playlist?list=PLYE0XunAbwfDvfabOlNWLViRcMI54M6CR)
