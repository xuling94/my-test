import sys
import time


class process_bar(object):

    """ echo process bar """

    def __init__(self, count=0, total=0, width=50):
        self._count = count
        self._total = total
        self._width = width


    def move(self, count):
        self._count = count


    def echo(self):
        total = self._total
        count = self._count
        width = self._width
        process = count * width / total
        length = len(str(total)) * 2 + width + 6 

        self._clear_buff(length)
        sys.stdout.write('  {0}/{1}  '.format(count, total))
        sys.stdout.write('=' * process + '>\r')

        if process == width:
            sys.stdout.write('\n')
        sys.stdout.flush()


    def _clear_buff(self, length):
        sys.stdout.write(' ' * length + '\r')
        sys.stdout.flush()


if __name__ ==  "__main__":
    probar = process_bar(total=10)
    for i in range(10):
        probar.move(count=i)
        probar.echo()
        time.sleep(1)
