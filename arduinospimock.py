from arduino.arduinospi import ArduinoSpi


class PortMock:

    def __init__(self, port='COM5', baudrate=115200, parity='N', bytesize=8, stopbits=1, timeout=1):
        self.port = port
        self.baudrate = baudrate
        self.parity = parity
        self.bytesize = bytesize
        self.stopbits = stopbits
        self.timeout = timeout

    def close(self):
        return True

    def write(self, command):
        print(f'PortMock write: {command.strip()}')
        return len(command)

    def read_all(self):
        answer = 'answer'
        print(f'PortMock read_all: {answer}')
        return answer

    @property
    def in_waiting(self):
        return 10

    @property
    def is_open(self):
        return True


class ArduinoSpiMock(ArduinoSpi):

    def __init__(self, *args, **kwargs):
        self._port = PortMock()
        self._name = 'SPI-mock'
        self._delay = 0
