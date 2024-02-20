import os
import sys
import traceback
from typing import Dict
from helang.lexer import Lexer
from helang.parser import Parser
from helang.exceptions import HeLangException
from helang.u8 import U8
SHELL_HELP = """
.help   Print this help message
.exit   Exit the shell
.env    Print current environments
""".strip()


def process_shell_keywords(text: str, env: Dict[str, U8]):
    if text == 'help':
        print(SHELL_HELP)
    elif text == 'exit':
        print('Saint He bless you.')
        sys.exit(0)
    elif text == 'env':
        for k, v in env.items():
            print(f'{k}: {v}')
    else:
        print(f'Invalid shell keyword: {text}')


def shell():
    env = dict()
    print('HeLang 1.0 | packaged by Saint He. | (main, Feb 20 2024, 00:00:00) on win32\nType ".help" for help.')
    while True:
        text = ''
        try:
            text = input('>>> ').strip()
        except (EOFError, KeyboardInterrupt):
            process_shell_keywords('exit', env)
        if text == '':
            continue
        if text.startswith('.'):
            process_shell_keywords(text[1:], env)
            continue
        if not text.endswith(';'):
            text += ';'
        lexer = Lexer(text)
        parser = Parser(lexer.lex())
        try:
            parser.parse().evaluate(env)
        except HeLangException:
            traceback.print_exc()
        except Exception as e:
            print("SaintHe: fatal error: Revise Saint He's videos.")
            raise e


def run(filepath: str):
    if not os.path.exists(filepath):
        print(
            f"SaintHe: fatal error: {filepath}: No such file or directory\ncompilation terminated.")
        sys.exit(-1)
    with open(filepath, 'r') as f:
        content = f.read()
    lexer = Lexer(content)
    parser = Parser(lexer.lex())
    env = dict()
    parser.parse().evaluate(env)


def main():
    if len(sys.argv) == 1:
        shell()
    else:
        run(sys.argv[-1])


if __name__ == '__main__':
    main()
