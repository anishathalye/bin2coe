import sys
from argparse import ArgumentParser
from typing import NoReturn

from bin2coe.convert import convert


def main() -> None:
    parser = ArgumentParser()
    parser.add_argument("-i", "--input", type=str, required=True, help="input filename")
    parser.add_argument("-o", "--output", type=str, required=True, help="output filename")
    parser.add_argument("-w", "--width", type=int, required=True, help="block memory width in bits")
    parser.add_argument("-d", "--depth", type=int, help="block memory depth in blocks")
    parser.add_argument("-f", "--fill", type=str, help="value to fill in empty words")
    parser.add_argument("-r", "--radix", type=int, default=16, help="fill radix and output radix")
    parser.add_argument("--big-endian", action="store_true", default=False, help="big endian mode")
    parser.add_argument("--mem", action="store_true", default=False, help="output mem file")
    options = parser.parse_args()

    # check radix
    if not (2 <= options.radix <= 36):  # noqa: PLR2004
        error("unsupported radix, must be between 2 and 36")
    if options.mem and options.radix not in [2, 16]:
        error("mem requires radix 2 or 16")

    # check width
    if not options.width >= 8:  # noqa: PLR2004
        error("width must be >= 8")
    if options.width & options.width - 1 != 0:
        error("width must be a power of 2")

    # if fill is specified, then depth must be specified too; otherwise, depth
    # can be inferred.
    if options.fill is not None and options.depth is None:
        error("depth must be specified if fill is specified")

    # calculate fill
    fill = None
    if options.fill is not None:
        try:
            fill = int(options.fill, options.radix)
        except ValueError:
            error(f"invalid fill ({options.fill}) for radix ({options.radix})")

    with open(options.input, "rb") as f:
        data = f.read()
    bits = 8 * len(data)

    # infer / validate depth
    depth = options.depth
    if depth is None:
        # infer depth if necessary, adding zero words if necessary
        if bits % options.width != 0:
            extra = options.width - bits % options.width
            if extra % 8 != 0:
                error(f"cannot infer depth, {bits} total bits, width {options.width}")
            extra_words = extra // 8
            data = data + bytes(extra_words)
            bits = 8 * len(data)
        depth = bits // options.width
    elif fill is None:
        if bits != options.width * depth:
            error(f"memory size / file size mismatch: {depth} x {options.width} bit != {bits}")
    else:
        # make sure it fills an integer number of words
        if bits % options.width != 0:
            error("data must fill an integer number of words")
        if bits > options.width * depth:
            error(f"memory size too small: {depth} x {options.width} bit < {bits}")

    with open(options.output, "wb") as f:
        convert(
            f,
            data,
            options.width,
            depth,
            fill,
            options.radix,
            little_endian=(not options.big_endian),
            mem=(options.mem),
        )


def error(msg: str) -> NoReturn:
    print(f"error: {msg}", file=sys.stderr)  # noqa: T201
    sys.exit(1)
