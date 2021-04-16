# Datamax python adapter

This piece of code allows you to control a datamax-o'neil label printer. You do not need knowledge of the datamax
programming language for simple tasks, this module takes care of it.

The module was developed and tested on python 3.6 using a datamax o'neil e-class mark III printer. It still has very
limited functionality allowing you to print text labels,QR-codes and Barcodes. In case you need any other features feel free to
contribute.

## Install

```bash
$ pip install datamax-printer
```

or from source:

```bash
$ python setup.py install
```

## Getting started

```python
from datamax_printer import DPLPrinter

printer = DPLPrinter('<ip of the printer>')
printer.configure()
printer.start_document()
printer.set_qr_code(285, 120, 'https://www.innetag.ch/', 9)
printer.set_label(300, 60, 'innetag.ch', 9, 10)
printer.set_barcode('0266','0025','1039001234',1)
printer.print()
```

Please check the `example.py` file in [our GitHub repository](https://github.com/inNETMonitoring/datamax-python-adapter)
for a working example.

## Ressources

In case you need more information about the datamax programming language, please check the [official DPL documentation](
https://support.honeywellaidc.com/s/article/How-To-Program-Using-The-Datamax-Programming-Language-Manual). It also
contains information about the different fonts available (see Appendix C).
