from time import sleep
import threading


class MultiplexThread(threading.Thread):
    stopped = None

    def __init__(self, displays_manager):
        threading.Thread.__init__(self)

        self.stopped = False
        self.manager = displays_manager
        self.sleep = 0.005

    def run(self):
        self._start()

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
