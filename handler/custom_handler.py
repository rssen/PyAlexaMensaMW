from typing import List, Sequence, Dict, Optional
import datetime
from random import randint

from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response

from handler.xml_parser import Dish
from ask_sdk_core.utils import is_intent_name, get_slot_value
from ask_sdk_core.skill_builder import SkillBuilder

sb = SkillBuilder()


def get_requested_day(day_slot: str, is_next_week: bool) -> datetime.date:
    pass


class ConnectionClause:
    def __init__(self):
        self.last_indices: Dict = {}

    @staticmethod
    def _get_random_non_repeating_element(li: List, last_index: Optional[int]):
        if last_index is None:
            random_index = randint(0, len(li) - 1)
        else:
            random_index = None
            while last_index == random_index or random_index is None:
                random_index = randint(0, len(li) - 1)
        random_element = li[random_index]
        return random_element, random_index

    def get_category_speech_output(self, category_name: str, dishes: List[Dish]) -> str:

        dishes_description = [dish.description[: dish.description.index("(")] for dish in dishes]

        category_intro = [
            f" In der Katgorie {category_name} gibt es {str.join(' ', dishes_description)} ",
            f" Die Kategorie {category_name} hält heute {str.join(' ', dishes_description)} bereit ",
            f" Bei {category_name} gibt es: {str.join(' ', dishes_description)}",
        ]

        speech_output, index = self._get_random_non_repeating_element(
            category_intro, self.last_indices.get("category", None)
        )
        self.last_indices["category"] = index
        return speech_output


def get_list_speech_output(dishes: List[Dish]):

    clause = ConnectionClause()

    # sort dishes by category and create a list for each category
    categories: Dict[str, List[Dish]] = {}
    for dish in dishes:
        if dish.category not in categories.keys():
            categories[dish.category] = [dish]
        else:
            categories[dish.category].append(dish)

    # generate speech output for each category
    combined_speech_output = ""
    for category_name, category_dishes in categories.items():
        combined_speech_output += (
            f" {clause.get_category_speech_output(category_name, category_dishes)}"
        )

    return combined_speech_output


class DayIntentHandler(AbstractRequestHandler):

    dishes: Sequence[Dish]

    def can_handle(self, handler_input: HandlerInput) -> bool:
        return is_intent_name("DayIntent")(handler_input)

    def handle(self, handler_input: HandlerInput) -> Response:
        # get slot value
        day_slot = get_slot_value(handler_input=handler_input, slot_name="day").capitalize()
        print(day_slot)
        day_name = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]
        day_of_week = datetime.date.today().weekday()
        try:
            day_slot_number = day_name.index(day_slot)
        except Exception as e:
            print(e)

        handler_input.response_builder.speak(f"Gewählter Tag: {day_slot}")
        return handler_input.response_builder.response


class DayAndCategoryIntentHandler(AbstractRequestHandler):

    dishes: Sequence[Dish]

    def can_handle(self, handler_input: HandlerInput) -> bool:
        return is_intent_name("DayAndCategoryIntent")(handler_input)

    def handle(self, handler_input: HandlerInput) -> Response:
        # get slot value
        day_slot = get_slot_value(handler_input=handler_input, slot_name="day").capitalize()
        is_next_week_slot = (
            get_slot_value(handler_input=handler_input, slot_name="is_next_week") == "true"
        )
        category_slot = get_slot_value(handler_input=handler_input, slot_name="category").lower()

        requested_date = get_requested_day(day_slot, is_next_week_slot)

        dishes_for_category_and_date = [dish for dish in self.dishes if dish.day == requested_date]
        speech_output = get_list_speech_output(dishes_for_category_and_date)

        handler_input.response_builder.speak(speech_output)
        return handler_input.response_builder.response
