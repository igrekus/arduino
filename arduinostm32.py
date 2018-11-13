from serial import Serial


class ArduinoSTM32(object):

    command_write_lpf_code = 'LPF'

    def __init__(self, *args, **kwargs):
        self._port = Serial(*args, **kwargs)

        self._name = 'STM32'

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
        print(f'{self._name} query: {question}')
        self.write(question)
        while not self._port.in_waiting:
            pass
        return self.read_all()

    def disconnect(self):
        print(f'{self._name}: disconnect()')
        self._port.close()

    def set_lpf_code(self, code: int) -> bool:
        print(f'{self._name}: set_lpf_code({code})')
        comm = f'{self.command_write_lpf_code},{code}'
        self.query(comm)
        return True

    @property
    def name(self):
        return f'{self._name} at {self._port.port}'

