import globalvar
from util import color


def show(s, p=0.):
    length = int(globalvar.columns / 4)
    print(f'\r{s}\t' +
          ('[{:' + str(length) + '}]').format(int(length * p) * '#') +
          color.render(f'\t{str(round(p * 100, 2))}%', 'INF'),
          end='')
