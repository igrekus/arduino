from arduino.arduinostm32 import ArduinoSTM32


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

    def write(self, command: str):
        cmd = (command + '\n').encode('ascii')
        print(f'PortMock write: {cmd.strip()}')
        return len(cmd)

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


class ArduinoSTM32Mock(ArduinoSTM32):

    def __init__(self, *args, **kwargs):
        self._port = PortMock()
        self._name = 'STM32-mock'

