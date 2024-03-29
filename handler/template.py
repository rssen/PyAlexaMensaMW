import abc
from abc import ABCMeta
from random import randint
from string import Template
from typing import Dict

from handler.context import Localization
from handler.error import Location, Severity, SkillException
from handler.logger import log_exception


def template_factory(language: Localization) -> "AbstractOutputTemplate":
    if language == Localization.GERMAN:
        return GermanOutputTemplate()

    log_exception(
        SkillException(
            f"Localization {language} not supported; fallback to german",
            Severity.WARNING,
            Location.OUTPUT_TEMPLATE,
        )
    )
    return GermanOutputTemplate()


class AbstractOutputTemplate(metaclass=ABCMeta):
    def __init__(self) -> None:
        self.__elements: Dict[int, int] = {}

    @abc.abstractmethod
    def get_connection_phrase(self) -> Template:
        pass

    @abc.abstractmethod
    def get_category_phrase(self) -> Template:
        pass

    @abc.abstractmethod
    def get_error_category_empty_at_date(self) -> Template:
        pass

    @abc.abstractmethod
    def get_error_no_dishes_at_date(self) -> Template:
        pass

    # returns a random element out of the range(list_length). For added output diversity,
    # the index is checked against the element dict, where the key is the list_length and the
    # value the last returned index for a list of that length.
    # For this purpose it is not relevant if those were the same lists.
    def _get_random_element(self, list_length: int) -> int:
        if list_length == 0:
            raise SkillException(
                "cannot get random index for empty list", Severity.FATAL, Location.OUTPUT_TEMPLATE
            )
        if list_length == 1:
            return 0

        if list_length in self.__elements:
            prev_length = self.__elements[list_length]
            while random_index := randint(0, list_length - 1):
                if not prev_length == random_index:
                    break
        else:
            random_index = randint(0, list_length - 1)
        self.__elements[list_length] = random_index
        return random_index


class GermanOutputTemplate(AbstractOutputTemplate):
    def get_connection_phrase(self) -> Template:
        connection_word = [
            Template("${phrase_1} und ${phrase_2}"),
            Template("${phrase_1} sowie ${phrase_2}"),
            Template("sowohl ${phrase_1} als auch ${phrase_2}"),
        ]
        random_index = self._get_random_element(len(connection_word))
        return connection_word[random_index]

    def get_category_phrase(self) -> Template:
        category_intro = [
            Template("In der Kategorie ${category_name} gibt es ${dishes}."),
            Template("Die Kategorie ${category_name} hält ${dishes} bereit."),
            Template("Bei ${category_name} gibt es: ${dishes}."),
        ]
        random_index = self._get_random_element(len(category_intro))
        return category_intro[random_index]

    def get_error_category_empty_at_date(self) -> Template:
        return Template("Die Kategorie ${category} enthält keine Gerichte am ${requested_date}.")

    def get_error_no_dishes_at_date(self) -> Template:
        return Template("Der Speiseplan enthält keine Gerichte am ${requested_date}.")
