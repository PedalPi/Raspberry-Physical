# Copyright 2017 SrMouraSilva
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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
            display._rewrite()
            display.on()
            sleep(self.sleep)
            display.off()

    def stop(self):
        self.stopped = True
        self._display_thread.stop()
