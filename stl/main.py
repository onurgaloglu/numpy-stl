import sys
from . import stl
import argparse


def _get_parser(description):
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r'),
                        default=sys.stdin, help='STL file to read')
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'),
                        default=sys.stdout, help='STL file to write')
    parser.add_argument('--name', nargs='?', help='Name of the mesh')
    parser.add_argument(
        '-n', '--use-file-normals', action='store_true',
        help='Read the normals from the file instead of recalculating them')
    return parser


def _get_name(args):
    if args.name:
        name = args.name
    elif not getattr(args.outfile, 'name', '<').startswith('<'):
        name = args.outfile.name
    elif not getattr(args.infile, 'name', '<').startswith('<'):
        name = args.infile.name
    else:
        name = None
    return name


def main():
    parser = _get_parser('Convert STL files from ascii to binary and back')
    parser.add_argument('-a', '--ascii', action='store_true',
                        help='Write ASCII file (default is binary)')
    parser.add_argument('-b', '--binary', action='store_true',
                        help='Force binary file (for TTYs)')

    args = parser.parse_args()
    name = _get_name(args)
    stl_file = stl.StlMesh(filename=name, fh=args.infile,
                           calculate_normals=False)

    if args.binary:
        mode = stl.BINARY
    elif args.ascii:
        mode = stl.ASCII
    else:
        mode = stl.AUTOMATIC

    stl_file.save(name, args.outfile, mode=mode,
                  calculate_normals=not args.use_file_normals)


def to_ascii():
    parser = _get_parser('Convert STL files to ASCII (text) format')
    args = parser.parse_args()
    name = _get_name(args)
    stl_file = stl.StlMesh(filename=name, fh=args.infile,
                           calculate_normals=False)
    stl_file.save(name, args.outfile, mode=stl.ASCII,
                  calculate_normals=not args.use_file_normals)


def to_binary():
    parser = _get_parser('Convert STL files to ASCII (text) format')
    args = parser.parse_args()
    name = _get_name(args)
    stl_file = stl.StlMesh(filename=name, fh=args.infile,
                           calculate_normals=False)
    stl_file.save(name, args.outfile, mode=stl.BINARY,
                  calculate_normals=not args.use_file_normals)

