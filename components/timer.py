from protocols import BusProtocol


class Timer:
    """
    Generates interrupts at regular intervals.

    The timer is clocked at 4096 Hz, which means that it increments its
    counter 4096 times per second. When the counter overflows (i.e.,
    gets bigger than FFh, which is 255 in decimal), it is reset to the
    current value of the TIMA register and an interrupt is requested.
    The frequency of the timer can be changed by writing different
    values to the TAC register.
    """

    div: int = 0
    tac: int = 0
    tma: int = 0
    tima: int = 0

    def run(self, bus: BusProtocol):
        cycles = 0

        while True:
            cycles += yield

            if cycles >= 4:
                self.div += 1
                cycles = 0

            if self.tac & 0b100:

                if self.tac & 0b1:
                    if self.div % 64 == 0:
                        self.tima += 1

                elif self.tac & 0b10:
                    if self.div % 16 == 0:
                        self.tima += 1

                elif self.tac & 0b11:
                    if self.div % 4 == 0:
                        self.tima += 1

                if self.tima > 0xFF:
                    self.tima = self.tma
                    bus.request_interrupt(2)
