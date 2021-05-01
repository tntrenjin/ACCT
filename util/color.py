__colors = {'WA': '\u001b[31m', 'AC': '\u001b[32m', 'RE': '\u001b[33m',
            'OK': '\u001b[32m', 'MF': '\u001b[31m', 'INF': '\u001b[33;1m',
            'INF_BG': '\u001b[1;37;42m', 'LB': '\u001b[30;1m', 'Reset': '\u001b[0m'}


def render(s, color):
    return f'{__colors[color]}{str(s)}{__colors["Reset"]}'
