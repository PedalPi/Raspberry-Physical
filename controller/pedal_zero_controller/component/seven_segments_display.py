from physical.controller.pedal_zero_controller.component.display import Display
from physical.component.sevensegments.seven_segments import SevenSegmentsBoard


class SevenSegmentsDisplay(Display):

    def __init__(self, a, b, c, d, e, f, g, dp, common_unit, common_tens):
        self.board = SevenSegmentsBoard(a=a, b=b, c=c, d=d, e=e, f=f, g=g)
        self.board.add_display(common=common_unit, anode=False)
        self.board.add_display(common=common_tens, anode=True)

    def show_effect(self, effect):
        if effect is None:
            self.board.value = '--'
        else:
            self.board.value = effect.patch.index

    def show_param(self, param):
        pass
