import win32print


class DPLPrinter:
    SOH = '\x01'
    STX = '\x02'

    command_mode = True

    def __init__(self, printer_name, document_name='datamax printer'):
        self.printer = win32print.OpenPrinter(printer_name)
        self.document_name = document_name
        win32print.StartDocPrinter(self.printer, 1, (document_name, None, 'RAW'))
        win32print.StartPagePrinter(self.printer)

    def __send_to_printer(self, command: str):
        print('Sent: ' + command)
        return win32print.WritePrinter(self.printer, command.encode('ASCII'))

    def __send_font(self, rotation: int, width_multiplier: int, height_multiplier: int, font_id: int, x_pos: int,
                    y_pos: int, text: str):
        # Adjust lengths
        font_id = str(font_id)
        while len(font_id) < 3:
            font_id = '0' + font_id

        x_pos = str(x_pos)
        while len(x_pos) < 4:
            x_pos = '0' + x_pos

        y_pos = str(y_pos)
        while len(y_pos) < 4:
            y_pos = '0' + y_pos

        data = str(rotation) + str(9) + str(width_multiplier) + str(height_multiplier) + font_id + x_pos + y_pos + \
               text + '\n'

        print('Sent: ' + data)
        return win32print.WritePrinter(self.printer, data.encode('ASCII'))

    def start_document(self):
        if not self.command_mode:
            raise RuntimeError('Already in label formatting mode')
        success = False
        if self.command_mode and self.__send_to_printer(f'{self.STX}L') == 2:
            self.__send_to_printer('D11')
            self.command_mode = False
            success = True
        return success

    def configure(self, start_print_position=220, imperial=False):
        if not self.command_mode:
            raise RuntimeError('Cannot configure label in label formatting mode')
        if imperial:
            self.__send_to_printer(f'{self.STX}n')
        else:
            self.__send_to_printer(f'{self.STX}m')

        sop = str(start_print_position)
        while len(sop) < 4:
            sop = '0' + sop
        self.__send_to_printer(f'{self.STX}O{sop}')

    def set_text(self, x_pos, y_pos, text, font_id, font_size):
        return self.__send_font(1, 1, 1, font_id, x_pos, y_pos, text)

    def print(self):
        self.__send_to_printer('E')
        win32print.EndDocPrinter(self.printer)
        win32print.StartDocPrinter(self.printer, 1, (self.document_name, None, 'RAW'))
        win32print.StartPagePrinter(self.printer)


def main():
    printer = DPLPrinter('Datamax Text Interface')
    printer.configure()
    printer.start_document()
    printer.set_text(10, 20, 'Hallo Welt', 80, 1)
    printer.print()


if __name__ == '__main__':
    main()
