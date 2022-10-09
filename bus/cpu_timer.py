class Timer:
    """The CPU timer, which is used to generate interrupts at regular intervals. The timer is clocked at 4096 Hz,
    which means that it increments its counter 4096 times a second. When the counter overflows (gets bigger than FFh)
    it will be reset to the current value of the TIMA register, and an interrupt will be requested, as described
    above. The frequency of the timer can be changed by writing different values to the TAC register. """

    div: int = 0
    tima: int = 0
    tma: int = 0
    tac: int = 0