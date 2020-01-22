from arduino.arduinospi import ArduinoSpi
from arduino.arduinoparallel import ArduinoParallel
from arduino.portmock import PortMock


class ProgrammerFactory:
    def __init__(self, port, label='Программатор'):
        self._port = port
        self._serial = None
        self._label = label
        self.addr = port

    def find_spi(self):
        return ArduinoSpi.find()

    def find_parallel(self):
        return ArduinoParallel.find()

    def from_address(self):
        ard = ArduinoParallel.from_address(self._port)
        if not ard:
            ard = ArduinoSpi.from_address(self._port)
            if not ard:
                ard = ArduinoParallel(PortMock())
        return ard

    def find(self):
        ard = self.find_spi()
        if not ard:
            ard = self.find_parallel()
            if not ard:
                ard = ArduinoParallel(PortMock())
        return ard

