import argparse
from datamax_printer import DPLPrinter


def main():
    parser = argparse.ArgumentParser(description='Example program on how to control a DPL printer with the datamax_'
                                                 'printer module')

    parser.add_argument('ip', help='IP address or hostname of the datamax oneil printer in your network')
    parser.add_argument('--port', '-p', help='The port the printer listens (default: 9100)', type=int, default=9100)

    args = parser.parse_args()

    printer = DPLPrinter(args.ip, args.port)
    printer.configure()
    printer.start_document()
    printer.set_qr_code(285, 120, 'https://www.innetag.ch/', 9)
    printer.set_label(300, 60, 'innetag.ch', 9, 10)
    printer.print()


if __name__ == '__main__':
    main()
