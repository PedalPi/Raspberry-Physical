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

class TextWriteStrategy(object):

    @staticmethod
    def prepare_text(total_spaces, data_input):
        strategy = None

        if isinstance(data_input, int):
            strategy = IntegerTextWriteStrategy()
        else:
            strategy = StringTextWriteStrategy()

        return strategy.prepare(total_spaces, data_input)

    def complete_text(self, total_spaces, text, white_space):
        text = text[-total_spaces:]
        if len(text) < total_spaces:
            text = white_space * (total_spaces - len(text)) + text

        return text

    def prepare(self, total_spaces, data_input):
        raise NotImplementedError()


class StringTextWriteStrategy(TextWriteStrategy):

    def prepare(self, total_spaces, data_input):
        """
        if text > total displays, truncate. Text will be the
        last len(total displays) characters

        if text < total displays, add space (' ') in left

        :param int total_spaces: Total text spaces in display
        :param string data_input: Text will be prepared
        :return: text prepared
        """
        return self.complete_text(total_spaces, data_input, ' ')


class IntegerTextWriteStrategy(TextWriteStrategy):

    def prepare(self, total_spaces, data_input):
        """
        if text > total displays, truncate. Text will be the
        last len(total displays) characters

        if text < total displays, add space ('0') in left

        :param int total_spaces: Total text spaces in display
        :param string data_input: Text will be prepared
        :return: text prepared
        """
        return self.complete_text(total_spaces, str(data_input), '0')
