# noPseudo
Translates pseudo-instructions in MIPS assembly to basic instructions. Only useful when your homework asks you not to use pseudo-instructions(that is, this repo is useless at all).

## IMPORTANT
1. The translator uses $at register for translation, make sure that the translated code is checked!
2. Edit translations in pseudo_settings.py.
3. Use at your own risk.

## Usage
```shell
$ python3 main.py -f filename_to_code.s
```