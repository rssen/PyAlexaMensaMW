from typing import Sequence

from handler.xml_parser import parse_xml


class Borg:
    _shared_state = {}

    def __init__(self):
        self.__dict__ = self._shared_state


class Context(Borg):
    dishes = None

    def __init__(self, menu_url: str = None):
        Borg.__init__(self)
        if menu_url is not None:
            self.dishes = parse_xml(menu_url)
