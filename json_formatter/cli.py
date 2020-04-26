#!/usr/bin/env python3
'''
format json
'''
import argparse

from logic import format_json_stream


def add_arguments(parser):
    parser.add_argument('-s', '--sort_keys', action='store_true',
                        help='sort keys')

    parser_group = parser.add_mutually_exclusive_group()
    parser_group.add_argument('-c', '--compact', action='store_true',
                              help='generate compact json')
    parser_group.add_argument('-i', '--indent', type=int, help='indent size')
    parser.add_argument('json_in', type=argparse.FileType(),
                        help='json file to format. use - to read from stdin')
    parser.add_argument('json_out', type=argparse.FileType('w'),
                        help='file to save the output. use - to write to '
                        'stdout')


def main(args=None):
    parser = argparse.ArgumentParser(description=__doc__)
    add_arguments(parser)

    args = parser.parse_args(args)
    args = dict(vars(args))
    with args.pop('json_in') as stream_in, args.pop('json_out') as stream_out:
        error = format_json_stream(stream_in, stream_out, **args)
        if error:
            print(error)
            exit(1)


if __name__ == '__main__':
    main()
