from time import sleep
from gpiozero.threads import GPIOThread


class MultiplexThread(object):
    stopped = None

    def __init__(self, displays_manager):
        self._display_thread = GPIOThread(
            target=self._start,
            args=()
        )

        self.stopped = False
        self.manager = displays_manager
        self.sleep = 0.005

    def start(self):
        self._display_thread.start()

    def _start(self):
        while not self.stopped:
            self.rewrite(self.manager.displays)

    def rewrite(self, displays):
        for display in displays:
            display.on()
            display._rewrite()
            sleep(self.sleep)
            display.off()

    def stop(self):
        self.stopped = True
