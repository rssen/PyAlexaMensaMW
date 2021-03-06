from typing import Sequence

from handler.xml_parser import parse_xml


class Borg:
    _shared_state = {}

    def __init__(self):
        self.__dict__ = self._shared_state


class Context(Borg):

    def __init__(self, dishes=None):
        Borg.__init__(self)
        if dishes is not None:
            self.dishes = dishes
