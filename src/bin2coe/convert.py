from typing import BinaryIO, Iterable, Iterator, List, Optional, TypeVar

T = TypeVar("T")


def chunks(it: Iterable[T], n: int) -> Iterator[List[T]]:
    res = []
    for elem in it:
        res.append(elem)
        if len(res) == n:
            yield res
            res = []
    if res:
        yield res


def word_to_int(word: List[int], *, little_endian: bool) -> int:
    if not little_endian:
        word = list(reversed(word))
    value = 0
    for i, byte in enumerate(word):
        value += byte << (8 * i)
    return value


def format_int(num: int, base: int, pad_width: int = 0) -> str:
    chars = "0123456789abcdefghijklmnopqrstuvwxyz"
    if num < 0:
        msg = "negative numbers not supported"
        raise ValueError(msg)
    res = []
    res.append(chars[num % base])
    while num >= base:
        num //= base
        res.append(chars[num % base])
    while len(res) < pad_width:
        res.append("0")
    return "".join(res[::-1])


def convert(
    output: BinaryIO,
    data: bytes,
    width: int,
    depth: int,
    fill: Optional[int],
    radix: int,
    *,
    little_endian: bool = True,
    mem: bool = False,
) -> None:
    pad_width = len(format_int(2**width - 1, radix))
    if not mem:
        output.write(f"memory_initialization_radix = {radix};\n".encode())
        output.write(b"memory_initialization_vector =\n")
    rows = 0
    for word in chunks(data, width // 8):
        if rows > 0:
            if not mem:
                output.write(b",")
            output.write(b"\n")
        output.write(format_int(word_to_int(word, little_endian=little_endian), radix, pad_width).encode("utf8"))
        rows += 1
    if rows < depth:
        if fill is None:
            msg = "fill must not be 'None' if memory is not filled by values"
            raise ValueError(msg)
        while rows < depth:
            if not mem:
                output.write(b",")
            output.write(b"\n")
            output.write(format_int(fill, radix, pad_width).encode("utf8"))
            rows += 1
    if not mem:
        output.write(b";")
    output.write(b"\n")
