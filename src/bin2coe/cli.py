from .convert import convert
from argparse import ArgumentParser
import sys


def main():
    parser = ArgumentParser()
    parser.add_argument('-i', '--input', type=str, required=True, help='input filename')
    parser.add_argument('-o', '--output', type=str, required=True, help='output filename')
    parser.add_argument('-w', '--width', type=int, required=True, help='block memory width in bits')
    parser.add_argument('-d', '--depth', type=int, help='block memory depth in blocks')
    parser.add_argument('-f', '--fill', type=str, help='value to fill in empty words')
    parser.add_argument('-r', '--radix', type=int, default=16, help='fill radix and output radix')
    parser.add_argument('--big-endian', action='store_true', default=False, help='big endian mode')
    options = parser.parse_args()

    # check radix
    if not (2 <= options.radix <= 36):
        error('unsupported radix, must be between 2 and 36')

    # check width
    if not 8 <= options.width:
        error('width must be >= 8')
    if not options.width & (options.width - 1) == 0:
        error('width must be a power of 2')

    # if fill is specified, then depth must be specified too; otherwise, depth
    # can be inferred.
    if options.fill is not None and options.depth is None:
        error('depth must be specified if fill is specified')

    # calculate fill
    fill = None
    if options.fill is not None:
        try:
            fill = int(options.fill, options.radix)
        except ValueError:
            error('invalid fill ({}) for radix ({})'.format(options.fill, options.radix))

    with open(options.input, 'rb') as f:
        data = f.read()
    bits = 8 * len(data)

    # infer / validate depth
    depth = options.depth
    if depth is None:
        # infer depth if necessary
        if bits % options.width != 0:
            error('cannot infer depth, {} total bits, width {}'.format(bits, options.width))
        depth = bits // options.width
    else:
        # validate depth
        if fill is None:
            if bits != options.width * depth:
                error('memory size / file size mismatch: {} x {} bit != {}'.format(depth, options.width, bits))
        else:
            # make sure it fills an integer number of words
            if bits % options.width != 0:
                error('data must fill an integer number of words')
            if bits > options.width * depth:
                error('memory size too small: {} x {} bit < {}'.format(depth, options.width, bits))

    with open(options.output, 'wb') as f:
        convert(f, data, options.width, depth, fill, options.radix, little_endian=(not options.big_endian))


def error(msg):
    print('error: {}'.format(msg), file=sys.stderr)
    exit(1)
