import serial
import time


class ArduinoSpi:
    command_write_lpf_code = 'LPF'
    command_start = '<'
    command_xra1405_write = 'x'
    command_separator = '.'
    command_end = '>'
    command_newline = '\n'
    command_set_p0_p7_output = '0C00'
    command_p0_p7_write = '04'

    def __init__(self, port):
        self._port = port
        self._name = 'SPI' if isinstance(self._port, serial.Serial) else 'SPI mock'
        self._delay = 0
        # self._delay = 0.2

    def __str__(self):
        return f'{self._name} at {self._port.port}'

    def write(self, command: str):
        cmd = command.encode('ascii')
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
        time.sleep(self._delay)
        return self.read_all()

    def disconnect(self):
        print(f'{self._name}: disconnect()')
        if self._port.is_open:
            self._port.close()

    def set_lpf_code_spi(self, code: int, address: int=0) -> bool:
        assert code in range(64)
        print(f'{self.__class__.__name__}: set_lpf_code_spi({code})')
        command = f'<l.{code}>'
        self.query(command)
        return True

    def set_lpf_code(self, code: int, address: int=0) -> bool:
        print(f'{self.__class__.__name__}: set_lpf_code_spi({code})')
        command = f'<l.{code}>'
        self.query(command)
        return True

    def set_lpf_code_spi_s_format(self, code: int, address: int) -> bool:
        print(f'{self.__class__.__name__}: set_lpf_code_spi({code})')
        command = f'<s.{code:02X}00000{address:X}>'
        self.query(command)
        return True

    def set_lpf_code_spi_s_format_reversed(self, code: int, address: int) -> bool:
        print(f'{self.__class__.__name__}: set_lpf_code_spi({code})')
        reverse = f"{int(''.join(reversed(f'{code:b}')), 2):X}"
        command = f'<s.{reverse}00000{address:X}>'
        self.query(command)
        return True

    def set_att_psm_code(self, att_code: int, psm_code: int) -> bool:
        assert att_code in range(64)
        assert psm_code in range(64)
        print(f'{self.__class__.__name__}: set_att_psm_code({att_code}, {psm_code})')
        command = f'<u.{att_code:02X}.{psm_code:02X}>'
        self.query(command)
        return True

    @property
    def name(self):
        return f'{self._name} at {self._port.port}'

    @classmethod
    def from_address(cls, port: str):
        return cls(serial.Serial(port=port, baudrate=115200, stopbits=serial.STOPBITS_ONE, bytesize=8,
                                 parity=serial.PARITY_NONE, timeout=0.5))

    @classmethod
    def find(cls):
        def available_ports():
            ports = list()
            for p in [f'COM{i+1}' for i in range(256)]:
                try:
                    s = serial.Serial(port=p, baudrate=115200)
                    s.close()
                    ports.append(p)
                except (OSError, serial.SerialException):
                    pass
            return ports

        for port in available_ports():
            s = serial.Serial(port=port, baudrate=115200, timeout=0.5)
            if s.is_open:
                s.write(b'<n>')
                ans = s.read(9)
                s.close()
                if b'SPI' in ans:
                    return ArduinoSpi.from_address(port)
        else:
            return None

    @property
    def status(self):
        return f'{self._name} at {self._port.port}'
