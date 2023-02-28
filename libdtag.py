class DoubanTagDict(object):

    def __init__(self):
        self.__size__ = 0
        self.__rank_dict__ = {}
        self.__name_dict__ = {}

    def __str__(self):
        return 'size: %d' % (self.__size__)

    def add(self, name):
        if self.seek(name) != None:
            pass
        else:
            dtag = DoubanTag()
            dtag.set(self.__size__, name)
            self.__rank_dict__[self.__size__] = dtag
            self.__name_dict__[name] = dtag
            self.__size__ += 1

    def seek(self, key):
        if isinstance(key, int):
            if key in self.__rank_dict__:
                return self.__rank_dict__[key]
            else:
                return None
        elif isinstance(key, str):
            if key in self.__name_dict__:
                return self.__name_dict__[key]
            else:
                return None
        else:
            return None

    def write_md(self, file):
        for i in range(self.__size__):
            dtag = self.seek(i)
            file.write(f'* {dtag}\n')


class DoubanTag(object):

    def __init__(self):
        self.__rank__ = 0
        self.__name__ = ''

    def __str__(self):
        return self.name()

    def __lt__(self, other):
        if isinstance(other, DoubanTag):
            return self.rank() < other.rank()
        else:
            return NotImplemented

    def set(self, rank, name):
        self.__rank__ = rank
        self.__name__ = name

    def rank(self):
        return self.__rank__

    def name(self):
        return self.__name__


# Global Access Part #
VERSION = '0.2'


def version():
    print('libdtag version: ' + VERSION)


if __name__ == '__main__':
    version()
