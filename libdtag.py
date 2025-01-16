# -*- coding: utf-8 -*-
# library for douban tag processing
import aiofiles
from dataclasses import dataclass


@dataclass(eq=True, order=True, unsafe_hash=True)
class DoubanTag:
    '''class for keeping track of an douban tag.'''
    rank: int
    name: str

    def __init__(self, rank: int = 0, name: str = ''):
        self.rank = rank
        self.name = name

    def __str__(self):
        return self.name


class DoubanTagDict(object):

    def __init__(self):
        self.__size__ = 0
        self.__section_dict__ = {}
        self.__rank_dict__ = {}
        self.__name_dict__ = {}

    def __str__(self):
        return 'size: %d' % (self.__size__)

    def add_section(self, section):
        if not self.__size__ in self.__section_dict__:
            self.__section_dict__[self.__size__] = [section]
        else:
            self.__section_dict__[self.__size__].append(section)

    def add_name(self, name):
        if self.seek(name) != None:
            pass
        else:
            dtag = DoubanTag(self.__size__, name)
            self.__rank_dict__[self.__size__] = dtag
            self.__name_dict__[name] = dtag
            self.__size__ += 1

    def add(self, name):
        self.add_name(name)

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

    async def write_md(self, filename):
        async with aiofiles.open(filename, mode='w') as file:
            for i in range(self.__size__):
                if i in self.__section_dict__:
                    if i > 0:
                        await file.write('\n')
                    for j in range(len(self.__section_dict__[i])):
                        await file.write(f'{self.__section_dict__[i][j]}\n')
                dtag = self.seek(i)
                await file.write(f'* {dtag}\n')


# Global Access Part #
VERSION = '0.4'


def version():
    print('libdtag version: ' + VERSION)


if __name__ == '__main__':
    version()
