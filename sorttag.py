# -*- coding: utf-8 -*-
# main function script
import argparse
import asyncio
import sys
import aiofiles
import libdtag


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('--tags_file', '-t', type=str, default='douban.md', help='douban tags file')
    parser.add_argument('--sep_char', '-s', type=str, default=' ', help='separator character used in io')
    parser.add_argument('--fileio', '-f', action=argparse.BooleanOptionalAction, help='use file io')
    parser.add_argument('--dump_tags', '-d', action=argparse.BooleanOptionalAction, help='dump tags to new markdown file')
    parser.add_argument('req_files', nargs='*')
    args = parser.parse_args()
    return args


async def load_douban_tags_async(tags_file: str, dump_tags: bool) -> libdtag.DoubanTagDict:
    db_tag_dict = libdtag.DoubanTagDict()
    async with aiofiles.open(tags_file, 'r') as file:
        async for line in file:
            if line.startswith('#'):
                db_tag_dict.add_section(line.strip('\n'))
            elif line.startswith('*'):
                name = line.strip('\n')[2 :]
                db_tag_dict.add(name)
    if dump_tags:
        await db_tag_dict.write_md(tags_file + '.new')
    return db_tag_dict


async def one_req_io(req: str, db_tag_dict: libdtag.DoubanTagDict, sep_char: str) -> str:
    names = req.strip('\n').split(sep_char)
    dtags = [db_tag_dict.seek(name) for name in names if db_tag_dict.seek(name) is not None]
    dtags = list(set(dtags))
    dtags.sort()
    return sep_char.join([str(tag) for tag in dtags])


async def one_file_io_async(req_file: str, db_tag_dict: libdtag.DoubanTagDict, sep_char: str) -> None:
    async with aiofiles.open(req_file) as f_in, aiofiles.open(req_file + '.out', 'w') as f_out:
        async for line in f_in:
            await f_out.write(await one_req_io(line, db_tag_dict, sep_char) + '\n')


def main() -> None:
    args = parse_args()
    db_tag_dict = asyncio.run(load_douban_tags_async(args.tags_file, args.dump_tags))
    if args.fileio and len(args.req_files) > 0:
        for req_file in args.req_files:
            asyncio.run(one_file_io_async(req_file, db_tag_dict, args.sep_char))
    else:
        for line in sys.stdin:
            print(asyncio.run(one_req_io(line, db_tag_dict, args.sep_char)))


if __name__ == '__main__':
    main()
