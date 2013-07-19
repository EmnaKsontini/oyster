# -*- coding: utf-8 -*-
"""

http://bit.ly/1baSfhM
"""

import shlex

# http://bit.ly/1baSfhM#tag_02_04
RESERVED_WORDS = frozenset([
    '!', '{', '}', 'case',
    'do', 'done', 'elif', 'else',
    'esac', 'fi', 'for', 'if',
    'in', 'then', 'until', 'while',
])


class Command(object):
    def __init__(self, program, arguments):
        self.options = {}
        self.program = program
        self.arguments = tuple(arguments)

        tokens = [self.program]
        tokens.extend(self.arguments)
        self.tokens = tuple(tokens)

        self.as_string = ' '.join(self.tokens)
        self._parse_options()

    def has_option(self, name):
        return name in self.options

    def get_option_values(self, name, *args):
        return self.options.get(name, *args)

    def get_option_count(self, name):
        values = self.get_option_values(name)
        if values:
            return len(values)
        return 0

    def __str__(self):
        return self.as_string

    def _parse_options(self):
        def sanitize_value(value):
            if not hasattr(value, 'isalpha'):
                return value

            if ((value.startswith('"') and value.endswith('"')) or
                (value.startswith("'") and value.endswith("'"))):
                value = value[1:-1]

            return value

        def get_value(next_token):
            if not next_token.startswith('-'):
                return sanitize_value(next_token)
            return True

        options = {}
        for index, token in enumerate(self.arguments):
            if not token.startswith('-'):
                continue

            try:
                next_token = self.arguments[index + 1]
            except IndexError:
                next_token = None

            if token.startswith('--'):
                key, _, value = token.partition('=')
                if value:
                    value = sanitize_value(value)
                else:
                    value = get_value(next_token)
                options.setdefault(key, []).append(value)
            else:
                keys = list(token[1:])
                for key in keys:
                    value = get_value(next_token)
                    options.setdefault('-' + key, []).append(value)

        self.options = options

def tokenize(string):
    return shlex.split(string, posix=True)


def is_comment(string):
    return string.lstrip()[0] == '#'


def is_script(string):
    tokens = string if hasattr(string, 'append') else tokenize(string)
    return tokens[0] in RESERVED_WORDS


def parse(string):
    if is_comment(string):
        return None

    tokens = tokenize(string)
    if not tokens:
        return None

    if is_script(tokens):
        return None

    command_tokens = []
    for index, token in enumerate(tokens):
        if token == '|':
            raise NotImplemented()
        elif token == '||':
            raise NotImplemented()
        elif token == '&&':
            raise NotImplemented()
        elif token == ';':
            raise NotImplemented()

        command_tokens.append(token)
    return Command(command_tokens[0], command_tokens[1:])
