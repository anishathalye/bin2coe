def chunks(it, n):
    res = []
    for elem in it:
        res.append(elem)
        if len(res) == n:
            yield res
            res = []
    if res:
        yield res

def word_to_int(word, little_endian):
    if not little_endian:
        word = reversed(word)
    value = 0
    for i, byte in enumerate(word):
        value += byte << (8*i)
    return value

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

def convert(output, data, width, depth, fill, radix, little_endian=True):
    pad_width = len(format_int(2**width-1, radix))
    output.write('memory_initialization_radix = {};\n'.format(radix).encode('utf8'))
    output.write(b'memory_initialization_vector =\n')
    rows = 0
    for word in chunks(data, width // 8):
        if rows > 0:
            output.write(b',\n')
        output.write(format_int(word_to_int(word, little_endian), radix, pad_width).encode('utf8'))
        rows += 1
    if rows < depth:
        assert fill is not None
    while rows < depth:
        output.write(b',\n')
        output.write(format_int(fill, radix, pad_width).encode('utf8'))
        rows += 1
    output.write(b';\n')
