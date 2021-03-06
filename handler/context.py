from enum import Enum
from typing import Sequence

from handler.xml_parser import parse_xml


class Localization(Enum):
    GERMAN = "german"


class Borg:
    _shared_state = {}

    def __init__(self):
        self.__dict__ = self._shared_state


class Context(Borg):
    dishes = None

    def __init__(self, menu_url: str = None, localization: Localization = Localization.GERMAN):
        Borg.__init__(self)
        if menu_url is not None:
            self.dishes = parse_xml(menu_url)
        self.localization = localization


