from component.Display import Display
from component.sevensegments.seven_segments import SevenSegmentsBoard


class SevenSegmentsDisplay(Display):

    def __init__(self, a, b, c, d, e, f, g, dp, common_unit, common_tens):
        self.board = SevenSegmentsBoard(a=a, b=b, c=c, d=d, e=e, f=f, g=g)
        self.board.add_display(common=common_unit, anode=False)
        self.board.add_display(common=common_tens, anode=True)

    def show_effect(self, effect):
        self.board.value = effect.patch.index

    def show_param(self, param):
        pass
