# -*- coding: utf-8 -*-


class AbstractConfigurationController(object):
    def onSelect(self):
        self.physical.toParamsController()

    def onNext(self):
        pass

    def onBefore(self):
        pass
