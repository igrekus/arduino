from time import sleep
from serial import Serial


class ArduinoSpi(object):

    command_write_lpf_code = 'LPF'
    command_start = '<'
    command_xra1405_write = 'x'
    command_separator = '.'
    command_end = '>'
    command_newline = '\n'
    command_set_p0_p7_output = '0C00'
    command_p0_p7_write = '04'

    def __init__(self, *args, **kwargs):
        self._port = Serial(*args, **kwargs)

        self._name = 'SPI'
        self._delay = 0.2

    def __str__(self):
        return f'{self._name} at {self._port.port}'

    def write(self, command: str):
        cmd = (command + '\n').encode('ascii')
        print(f'{self._name} write: {cmd.strip()}')
        return self._port.write(cmd)

    def read_all(self):
        answer = self._port.read_all()
        print(f'{self._name} read_all: {answer}')
        return answer

    def query(self, question: str):
        self.write(question)
        # while not self._port.in_waiting:
        #     pass
        sleep(self._delay)
        return self.read_all()

    def disconnect(self):
        print(f'{self._name}: disconnect()')
        if self._port.is_open:
            self._port.close()

    def set_lpf_code_spi(self, code: int) -> bool:
        print(f'{self._name}: set_lpf_code_spi({code})')
        command = \
            self.command_start + \
            self.command_xra1405_write + \
            self.command_separator + \
            self.command_set_p0_p7_output + \
            self.command_separator + \
            self.command_p0_p7_write + \
            f'{code:02X}' + \
            self.command_end + \
            self.command_newline
        self.query(command)
        return True

    def set_lpf_code_parallel(self, code: int) -> bool:
        print(f'{self._name}: set_lpf_code_parallel({code})')
        command = f'<l.{code}>'
        self.query(command)
        return True

    set_lpf_code = set_lpf_code_parallel

    @property
    def name(self):
        return f'{self._name} at {self._port.port}'

