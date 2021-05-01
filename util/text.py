import globalvar
from config import question_number, TIME_LIMIT


def clear_format(s):
    for i in [':', ',', '：', '，']:
        s = s.replace(i, ' ')
    for i in ['\r', '\n', ' ']:
        s = s.replace(i, '')

    return s


def generate_title_box():
    N = 70
    title = ''
    title += '┌' + '─' * N + '┐\n'
    title_buffer = ['AC: All correct', 'WA: Wrong answer',
                    'HC: The public test data passed, but the secret test data failed',
                    f'TL: Time limit ({TIME_LIMIT}s)', 'CE: Compile error', 'RE: Runtime error',
                    'MF: Missing file'
                    ]
    title += ''.join([("│  {:" + str(N - 4) + "s}  │\n").format(s) for s in title_buffer])
    title += '└' + '─' * N + '┘\n\n'

    globalvar.title_box_str = title


def generate_scoreboard_box(final_result):
    scoreboard_buffer = ['┌', '│', '├', '│', '└']
    for idx, r in enumerate(final_result[1:]):
        M = (len('Q' + str(idx + 1)) + 4)
        scoreboard_buffer[0] += '─' * M
        scoreboard_buffer[1] += f'  Q{idx + 1}  │'
        scoreboard_buffer[2] += '─' * M
        scoreboard_buffer[3] += f'  {final_result[idx + 1]}  │'
        scoreboard_buffer[4] += '─' * M

        if idx == question_number - 1:
            scoreboard_buffer[0] += '┐'
            scoreboard_buffer[2] += '┤'
            scoreboard_buffer[4] += '┘'
        else:
            scoreboard_buffer[0] += '┬'
            scoreboard_buffer[2] += '┼'
            scoreboard_buffer[4] += '┴'

    scoreboard = '\n'.join(scoreboard_buffer) + '\n\n'
    return scoreboard
