# bin2coe [![Build Status](https://github.com/anishathalye/bin2coe/workflows/CI/badge.svg)](https://github.com/anishathalye/bin2coe/actions?query=workflow%3ACI)

bin2coe is, as its name suggests, a tool to convert binary files to [COE] files
for initializing Xilinx FPGA block RAM.

Usage
-----

Basic usage looks like this:

```bash
bin2coe -i INPUT -w WIDTH -o OUTPUT
```

Additionally, you can specify depth manually (rather than having it be
inferred), specify a value to fill in empty words, and specify the radix. See
`bin2coe --help` for more information.

Installation
------------

bin2coe can be installed from [PyPI]:

```bash
pip install bin2coe
```

After running this command, the `bin2coe` binary should be available on your
`$PATH`.

License
-------

Copyright (c) Anish Athalye. Released under the MIT License. See
[LICENSE.md][license] for details.

[COE]: https://docs.xilinx.com/r/en-US/ug896-vivado-ip/COE-File-Syntax
[PyPI]: https://pypi.org/project/bin2coe/
[license]: LICENSE.md
