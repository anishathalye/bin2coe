def bits(data):
    for byte in data:
        for i in range(8):
            yield bool(byte & (1 << (7 - i)))

def chunks(it, n):
    res = []
    for elem in it:
        res.append(elem)
        if len(res) == n:
            yield res
            res = []
    if res:
        yield res

def bitsn(data, n):
    for word in chunks(bits(data), n):
        acc = 0
        for i, bit in enumerate(reversed(word)):
            acc += bit << i
        yield acc

def format_int(num, base, pad_width=0):
    chars = "0123456789abcdefghijklmnopqrstuvwxyz"
    if num < 0:
        return '-' + int2base(-num, base, chars)
    res = []
    res.append(chars[num % base])
    while num >= base:
        num //= base
        res.append(chars[num % base])
    while len(res) < pad_width:
        res.append('0')
    return ''.join(res[::-1])

def convert(output, data, width, depth, fill, radix):
    pad_width = len(format_int(2**width-1, radix))
    output.write('memory_initialization_radix = {};\n'.format(radix).encode('utf8'))
    output.write(b'memory_initialization_vector =\n')
    rows = 0
    for word in bitsn(data, width):
        if rows > 0:
            output.write(b',\n')
        output.write(format_int(word, radix, pad_width).encode('utf8'))
        rows += 1
    if rows < depth:
        assert fill is not None
    while rows < depth:
        output.write(b',\n')
        output.write(format_int(fill, radix, pad_width).encode('utf8'))
        rows += 1
    output.write(b';\n')
