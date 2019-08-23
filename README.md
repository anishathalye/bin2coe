bin2coe
=======

bin2coe is, as its name suggests, a tool to convert binary files to [COE] files
for initializing Xilinx FPGA block RAM.

---

[![Build Status](https://travis-ci.com/anishathalye/bin2coe.svg?branch=master)](https://travis-ci.com/anishathalye/bin2coe)

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

Packaging
---------

1. Update version information.

2. Build the package using ``python setup.py sdist bdist_wheel``.

3. Sign and upload the package using ``twine upload -s dist/*``.

License
-------

Copyright (c) 2019 Anish Athalye. Released under the MIT License. See
[LICENSE.md][license] for details.

[COE]: https://www.xilinx.com/support/documentation/sw_manuals/xilinx11/cgn_r_coe_file_syntax.htm
[PyPI]: https://pypi.org/project/bin2coe/
[license]: LICENSE.md
