import socket


class DPLPrinter:
    SOH = '\x01'
    STX = '\x02'

    command_mode = True

    def __init__(self, printer_ip, printer_port=9100):
        self.printer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection_info = (printer_ip, printer_port)
        self.printer.connect(self.connection_info)

    def __send_to_printer(self, command: str):
        print('Sent: ' + command)
        return self.printer.send(command.encode('ASCII'))

    def __adjust_number_length(self, value: str, length: int):
        while len(value) < length:
            value = '0' + value
        return value

    def start_document(self):
        """
        Sets the printer into label formating mode. Call this function before using set_label() or set_qr_code()
        :return: True if successful, False otherwise
        """
        if not self.command_mode:
            raise RuntimeError('Already in label formatting mode')
        success = False
        if self.command_mode and self.__send_to_printer(f'{self.STX}L') == 2:
            self.__send_to_printer('D11\x0D')
            self.command_mode = False
            success = True
        return success

    def configure(self, border_bottom=0, imperial=False):
        """
        :param border_bottom: The distance (in 0.1mm) from the bottom for labels. This value will be added to the
        y-coordinate every time you specify a label.
        If a value bellow 50 is passed, it is reset to the default value (the default values can be found in the DPL
        Guide).
        :param imperial: For those who like no SI measurements it is possible to set the printer to imperial mode.
        If this flag is true, al distances are passed in inches/100.
        :return:
        """
        if not self.command_mode:
            raise RuntimeError('Cannot configure printer label formatting mode')
        if imperial:
            self.__send_to_printer(f'{self.STX}n')
        else:
            self.__send_to_printer(f'{self.STX}m')

        sop = str(border_bottom)
        while len(sop) < 4:
            sop = '0' + sop
        self.__send_to_printer(f'{self.STX}O{sop}')

    def set_label(self, x_pos, y_pos, text, font_id, font_size, rotation=0):
        """
        :param x_pos: Position of the text label on the X-Axis (in 0.1mm)
        :param y_pos: Position of the text label on the Y-Axis (in 0.1mm)
        :param text: The text to print
        :param font_id:
        :param font_size:
        :return: Number of bytes sent to the printer
        """
        if self.command_mode:
            raise RuntimeError('Cannot print label in command mode')
        rot_value = 1  # default = no rotation
        if rotation == 90:
            rot_value = 2
        elif rotation == 180:
            rot_value = 3
        elif rotation == 270:
            rot_value = 4

        # Adjust lengths
        x_pos = self.__adjust_number_length(str(x_pos), 4)
        y_pos = self.__adjust_number_length(str(y_pos), 4)

        size = '000'
        width_multiplier = 1
        height_multiplier = 1
        if font_id == 9:
            size = 'A' + self.__adjust_number_length(str(font_size), 2)
        else:
            if len(font_size) == 2:
                width_multiplier = font_size[0]
                height_multiplier = font_size[1]

        data = str(rot_value) + str(font_id) + str(width_multiplier) + str(height_multiplier) + size + y_pos + x_pos + \
               text + '\x0D'

        return self.__send_to_printer(data)

    def set_qr_code(self, x_pos, y_pos, data, size=8):
        """
        Generates a QR-Code.
        :param x_pos: Position of the QR-Code on the X-Axis (in 0.1mm)
        :param y_pos: Position of the QR-Code on the Y-Axis (in 0.1mm)
        :param data: Data to be encoded in the QR-Code.
        (Numeric Data, Alphanumeric Data, 8-bit byte data or Kanji characters)
        :param size: Size of 1 dot in QR-Code (in 0.1mm) (1-37)
        :return: Number of bytes sent to the printer
        """
        if self.command_mode:
            raise RuntimeError('Cannot print qr-code in command mode')
        x_pos = str(x_pos)
        while len(x_pos) < 4:
            x_pos = '0' + x_pos

        y_pos = str(y_pos)
        while len(y_pos) < 4:
            y_pos = '0' + y_pos

        if size > 9:
            size = chr(ord('A') + (size - 10))

        command = f'1W1d{size}{size}000{y_pos}{x_pos}{data}\x0D\x0D'
        return self.__send_to_printer(command)

    def print(self):
        self.__send_to_printer('E')


def main():
    printer = DPLPrinter('10.0.50.111')
    printer.configure()
    printer.start_document()
    printer.set_qr_code(285, 120, 'https://www.innetag.ch/', 9)
    printer.set_label(300, 60, 'innetag.ch', 9, 10)
    printer.print()


if __name__ == '__main__':
    main()
