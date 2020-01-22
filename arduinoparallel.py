import time
import serial


class ArduinoParallel:

    command_write_lpf_code = 'LPF'

    def __init__(self, port):
        self._port = port

        self._name = 'Parallel' if isinstance(port, serial.Serial) else 'Parallel mock'
        self._delay = 0.3

    def __str__(self):
        return f'{self._name} at {self._port.port}'

    def write(self, command: str):
        cmd = bytes(f'{command}', encoding='ascii')
        print(f'>>> {self._name} write: {cmd.strip()}')
        return self._port.write(cmd)

    def read_all(self):
        answer = self._port.read_all()
        print(f'> {self._name} answer: {answer}')
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

    def set_lpf_code(self, code: int) -> bool:
        print(f'{self._name}: set_lpf_code dec={code}, bin={code:06b}')
        comm = f'{self.command_write_lpf_code},{code}'
        self.query(comm)
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
            s = serial.Serial(port=port, baudrate=115200, stopbits=serial.STOPBITS_ONE, bytesize=8,
                              parity=serial.PARITY_NONE, timeout=0.5)
            if s.is_open:
                s.write(b'#NAME')
                time.sleep(0.3)
                ans = s.read_all()
                s.close()
                if b'ARDUINO' in ans:
                    return port
        else:
            return ''

    @property
    def status(self):
        return f'{self._name} at {self._port.port}'
