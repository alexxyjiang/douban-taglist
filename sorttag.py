import argparse
import libdtag
import sys


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('--tags_file', '-t', type=str, default='douban.md', help='douban tags file')
    parser.add_argument('--sep_char', '-s', type=str, default=' ', help='separator character used in io')
    parser.add_argument('--fileio', '-f', action=argparse.BooleanOptionalAction, help='use file io')
    parser.add_argument('req_files', nargs='*')
    args = parser.parse_args()
    return args


def load_douban_tags(tags_file: str) -> libdtag.DoubanTagDict:
    db_tag_dict = libdtag.DoubanTagDict()
    for line in open(tags_file):
        if line.startswith('*'):
            name = line.strip('\n')[2 :]
            db_tag_dict.add(name)
    return db_tag_dict


def one_req_io(req: str, db_tag_dict: libdtag.DoubanTagDict, sep_char: str) -> str:
    names = req.strip('\n').split(sep_char)
    dtags = [db_tag_dict.seek(name) for name in names if db_tag_dict.seek(name) is not None]
    dtags = list(set(dtags))
    dtags.sort()
    return sep_char.join([str(tag) for tag in dtags])


def main() -> None:
    args = parse_args()
    db_tag_dict = load_douban_tags(args.tags_file)
    if args.fileio and len(args.req_files) > 0:
        for req_file in args.req_files:
            with open(req_file) as f_in, open(req_file + '.out', 'w') as f_out:
                for line in f_in:
                    f_out.write(one_req_io(line, db_tag_dict, args.sep_char) + '\n')
    else:
        for line in sys.stdin:
            print(one_req_io(line, db_tag_dict, args.sep_char))


if __name__ == '__main__':
    main()
