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

import time


def msleep(milliseconds):
    """Sleep the specified amount of milliseconds."""
    time.sleep(milliseconds / 1000.0)


def usleep(microseconds):
    """Sleep the specified amount of microseconds."""
    time.sleep(microseconds / 1000000.0)


class ByteUtil(object):

    @staticmethod
    def apply_flag(byte, flag, status):
        if status:
            byte |= flag
        else:
            byte &= ~flag

        return byte

    @staticmethod
    def is_flag_active(byte, flag):
        return (byte & flag) != 0
