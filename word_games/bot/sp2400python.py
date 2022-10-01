import serial


class sp2400python:
    # 40
    INITIALIZE = [0x1B, 0x40]

    # 23
    UNDERLINE_START = [0x1B, 0x2D, 0x01]
    UNDERLINE_END = [0x1B, 0x2D, 0x00]

    # 29-30
    ITALIC_START = [0x1B, 0x34]
    ITALIC_END = [0x1B, 0x35]

    # 33-34
    PAPER_OUT_DETECTION_OFF = [0x1B, 0x38]
    PAPER_OUT_DETECTION_ON = [0x1B, 0x39]

    # 46-47
    EMPHASIZED_START = [0x1B, 0x45]
    EMPHASIZED_END = [0x1B, 0x46]

    # 48-49
    DOUBLE_STRIKE_START = [0x1B, 0x47]
    DOUBLE_STRIKE_END = [0x1B, 0x48]

    # 60-61
    SUPERSCRIPT_START = [0x1B, 0x53, 0x00]
    SUBSCRIPT_START = [0x1B, 0x53, 0x01]
    SUPERSCRIPT_END = [0x1B, 0x54]
    SUBSCRIPT_END = SUPERSCRIPT_END

    # 62
    PRINTING_UNIDIRECTIONAL = [0x1B, 0x55, 0x01]
    PRINTING_BIDIRECTIONAL = [0x1B, 0x55, 0x00]

    # 63
    DOUBLE_WIDTH_START = [0x1B, 0x57, 0x01]
    DOUBLE_WIDTH_END = [0x1B, 0x57, 0x00]

    # 72
    FONT_SET = [0x1B, 0x6B]
    FONT_NLQ = [0x0]
    FONT_SANS_SERIF = [0x1]
    FONT_COURIER = [0x2]
    FONT_PRESTIGE = [0x3]
    FONT_SCRIPT = [0x4]
    FONT_GOTHIC = [0x7]

    # 77
    DOUBLE_HEIGHT_START = [0x1B, 0x77, 0x01]
    DOUBLE_HEIGHT_END = [0x1B, 0x77, 0x00]

    # 78
    QUALITY_DRAFT = [0x1B, 0x78, 0x00]
    QUALITY_NLQ = [0x1B, 0x78, 0x01]

    def __init__(self, port, baud=9600):
        self.ser = serial.Serial(port, baud, xonxoff=True)
        self.sendCommand(self.INITIALIZE)

    def print(self, text):
        tt = text.maketrans("ęĘóÓąĄśŚłŁżŻźŹćĆńŃ", "\x91\x90\xa2\xa3\x86\x8f\x9e\x98\x92\x9c\xa7\xa1\xa6\xa0\x8d\x95\xa4\xa5", "")
        text = text.translate(tt)
        self.ser.write(bytes(text, "charmap"))

    def printLine(self, text=""):
        self.print(text + "\r\n")

    def sendCommand(self, command):
        self.ser.write(bytes(command))

    def setFont(self, font):
        self.sendCommand(self.FONT_SET + font)

    def printCharTableSafe(self):
        # omit common control codes, CAN, ESC, DC2-DC4
        prohibited = list(range(0x07, 0x0F + 1)) + list(range(0x12, 0x14 + 1)) + [0x18, 0x1B]
        self.printCharTable(prohibited)

    def printCharTable(self, prohibited=None):
        if prohibited is None:
            prohibited = list()
        for i in range(0, 256):
            if i in prohibited:
                self.print(str(bytearray([i]).hex()) + " = XX\t")
            else:
                self.print(str(bytearray([i]).hex()) + " = ")
                self.sendCommand([i])
                self.print("\t")
        self.printLine()

    def __del__(self):
        self.ser.close()

if __name__ == "__main__":
    port = 5
    printer = sp2400python(f"/dev/ttyS{port}")

    fonts = {
        "NLQ": printer.FONT_NLQ,
        "SANS SERIF": printer.FONT_SANS_SERIF,
        "COURIER": printer.FONT_COURIER,
        "PRESTIGE": printer.FONT_PRESTIGE,
        "SCRIPT": printer.FONT_SCRIPT,
        "GOTHIC": printer.FONT_GOTHIC
    }

    printer.sendCommand(printer.QUALITY_NLQ)
    for key in fonts:
        printer.setFont(fonts[key])
        printer.printLine("Font demo of: " + key)
