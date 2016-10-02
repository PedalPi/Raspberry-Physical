import sys
from time import sleep


if sys.version_info >= (3, 0):
    from _thread import start_new_thread
else:
    from thread import start_new_thread


class MultiplexThread(object):
    stopped = None

    def __init__(self, displays_manager):
        self.stopped = False
        self.manager = displays_manager
        self.sleep = 0.005

    def start(self):
        start_new_thread(self._start, ())

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

