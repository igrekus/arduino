import time
import serial

IO1, \
IO2, \
IO3, \
IO4, \
IO5, \
IO6, \
IO7, \
IO8, \
IO9, \
IO10, \
IO11, \
IO12, \
IO13, \
IO14, \
IO15, \
IO16, \
IO17, \
IO18, \
IO19, \
IO20, \
IO21, \
IO22, \
IO23, \
IO24 = range(1, 25)

IO_OUT, IO_IN = 0, 1
PIN_OFF, PIN_ON = 0, 1

default_pin_io = {
    IO1: IO_OUT,
    IO2: IO_OUT,
    IO3: IO_OUT,
    IO4: IO_OUT,
    IO5: IO_OUT,
    IO6: IO_OUT,
    IO7: IO_OUT,
    IO8: IO_OUT,
    IO9: IO_OUT,
    IO10: IO_OUT,
    IO11: IO_OUT,
    IO12: IO_OUT,
    IO13: IO_OUT,
    IO14: IO_OUT,
    IO15: IO_OUT,
    IO16: IO_OUT,
    IO17: IO_OUT,
    IO18: IO_OUT,
    IO19: IO_OUT,
    IO20: IO_OUT,
    IO21: IO_OUT,
    IO22: IO_OUT,
    IO23: IO_OUT,
    IO24: IO_OUT
}

default_pin_states = {
    IO1: PIN_OFF,
    IO2: PIN_OFF,
    IO3: PIN_OFF,
    IO4: PIN_OFF,
    IO5: PIN_OFF,
    IO6: PIN_OFF,
    IO7: PIN_OFF,
    IO8: PIN_OFF,
    IO9: PIN_OFF,
    IO10: PIN_OFF,
    IO11: PIN_OFF,
    IO12: PIN_OFF,
    IO13: PIN_OFF,
    IO14: PIN_OFF,
    IO15: PIN_OFF,
    IO16: PIN_OFF,
    IO17: PIN_OFF,
    IO18: PIN_OFF,
    IO19: PIN_OFF,
    IO20: PIN_OFF,
    IO21: PIN_OFF,
    IO22: PIN_OFF,
    IO23: PIN_OFF,
    IO24: PIN_OFF
}

# matlab code bits -> normalized bits:
# 5 -> 0, 6 -> 1, 3 -> 2, 4 -> 3
b0, b1, b2, b3 = range(4)


class JeromeSerialMock:

    def __init__(self):
        self.port = 'COM1'
        self._open = True
        self._last_write = b''
        self._success = b'#OK\r\n'
        self._success_io_set = b'#IO,SET,OK\r\n'
        self._success_wra = b'#WRA,OK,24\r\n'
        self._success_wr = b'#WR,OK\r\n'

    def open(self):
        self._open = True

    def close(self):
        self._open = False

    def write(self, what):
        self._last_write = what

    def read_all(self):
        ans = b''
        if self._last_write == b'$KE\r\n':
            ans = self._success
        elif b'$KE,IO,SET,' in self._last_write:
            ans = self._success_io_set
        elif b'$KE,WRA,' in self._last_write:
            ans = self._success_wra
        elif b'$KE,WR,' in self._last_write:
            ans = self._success_wr
        self._last_write = b''
        return ans

    @property
    def is_open(self):
        return self._open


class Jerome:

    def __init__(self, serial_obj):
        self._serial = serial_obj

        self._name = 'Jerome'
        self._delay = 0.0

        self._pin_io = dict(default_pin_io)
        self._pin_states = dict(default_pin_states)

    def __str__(self):
        return f'{self._name} at {self._serial.port}'

    def write(self, command: str):
        cmd = (command + '\r\n').encode('ascii')
        return self._serial.write(cmd)

    def read_all(self):
        answer = self._serial.read_all().strip()
        return str(answer, encoding='UTF-8')

    def query(self, question: str):
        self.write(question)
        time.sleep(self._delay)
        return self.read_all()

    def close(self):
        if self._serial.is_open:
            self._serial.close()

    def ping(self):
        return self.query('$KE')

    def mkr_init(self):
        # TODO extract to a specialized subclass?
        ios = [self.set_io(pin, PIN_OFF) for pin in [IO7, IO8, IO9, IO10, IO11, IO12, IO13, IO14]]
        wra = self.write_array('000000010101010000000000')
        return ios + [wra]

    def set_io(self, pin, state):
        self._pin_io[pin] = state
        return self.query(f'$KE,IO,SET,{pin},{state}')

    def write_array(self, array):
        for line, state in enumerate(array):
            self._pin_states[line + 1] = int(state)
        return self.query(f'$KE,WRA,{array}')

    def write_line(self, line, state):
        self._pin_states[line] = state
        return self.query(f'$KE,WR,{line},{state}')

    @property
    def name(self):
        return self.__str__()

    @property
    def is_open(self):
        return self._serial.is_open

    @property
    def delay(self):
        return self._delay

    @delay.setter
    def delay(self, value):
        self._delay = value

    @property
    def pin_states(self):
        return self._pin_states

    @classmethod
    def find_com_port(cls):

        def available_ports():
            ports = list()
            for i in range(256):
                port = f'COM{i+1}'
                try:
                    s = serial.Serial(port=port, baudrate=115200)
                    s.close()
                    ports.append(port)
                except (OSError, serial.SerialException):
                    pass
            return ports

        for port in available_ports():
            s = serial.Serial(port=port, baudrate=115200)
            s.write(b'$KE\r\n')
            time.sleep(0.1)
            ans = s.read_all()
            if b'#OK' in ans:
                return cls(s)
        else:
            return None


