from typing import List, Sequence, Dict, Optional
import datetime
from random import randint

from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.handler_input import HandlerInput

from handler.xml_parser import Dish
from ask_sdk_core.utils import (
    is_intent_name,
    get_slot_value,
    get_slot,
)
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_model import Response, Slot

sb = SkillBuilder()


# returns the date of the requested day
def get_requested_day(day_slot: str, is_next_week: bool) -> datetime.date:
    day_of_week = datetime.date.today().weekday()
    day_name = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]
    today = datetime.date.today()

    if day_slot == "Heute":
        return today
    elif day_slot == "Morgen":
        return today + datetime.timedelta(days=1)  # return date of tomorrow
    elif day_slot == "Übermorgen":
        return today + datetime.timedelta(days=2)  # return date of tomorrow

    # day_slot is in Montag, ..., Sonntag

    requested_slot_number = day_name.index(day_slot)

    # requested day is in the next week (e.g. today is Mittwoch and Montag is requested)
    if requested_slot_number < day_of_week:
        is_next_week = True

    if not is_next_week:
        # return date that is part of the current week
        return today + datetime.timedelta(days=requested_slot_number - day_of_week)
    else:
        # return date that is part of the next week
        return today + datetime.timedelta(days=7 - day_of_week + day_name.index(day_slot))


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
            f"In der Kategorie {category_name} gibt es {str.join(', außerdem gibt es ', dishes_description)}.",
            f"Die Kategorie {category_name} hält {str.join(' sowie ', dishes_description)} bereit.",
            f"Bei {category_name} gibt es: {str.join(' ', dishes_description)}.",
        ]

        speech_output, index = self._get_random_non_repeating_element(
            category_intro, self.last_indices.get("category", None)
        )
        self.last_indices["category"] = index
        return speech_output


def get_list_speech_output(dishes: List[Dish]) -> str:

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

    # remove special caracters
    combined_speech_output = combined_speech_output.replace("&", "und")
    # (register new special caracters by adding lines here)
    # combined_speech_output = combined_speech_output.replace("old", "new")

    return combined_speech_output


def get_resolved_slot_value(slot: Slot, resolution_authority_name: str):

    slot_resolutions = slot.resolutions
    if slot_resolutions is None:
        raise AttributeError("Slot has no resolutions.")
    for authority in slot_resolutions.resolutions_per_authority:
        if authority.authority.find(resolution_authority_name) != -1:
            if len(authority.values) != 1:
                raise ValueError(
                    f"Expected one resolution for slot category, got {len(authority.values)}."
                )
            resolved_value_wrapper = authority.values[0]
            resolved_category_value = resolved_value_wrapper.to_dict()["value"]
            assert isinstance(resolved_category_value, dict)
            resolved_category = resolved_category_value["name"]
            assert isinstance(resolved_category, str)
            break
    else:
        raise ValueError(f"Could not find authority {resolution_authority_name}.")

    return resolved_category


class DayIntentHandler(AbstractRequestHandler):

    dishes: Sequence[Dish]

    def can_handle(self, handler_input: HandlerInput) -> bool:
         return is_intent_name("DayIntent")(handler_input)

    def handle(self, handler_input: HandlerInput) -> Response:
        
        # get slot value
        day_slot = get_slot(handler_input=handler_input, slot_name="day")
        resolved_day = get_resolved_slot_value(
            slot=day_slot, resolution_authority_name="TAG"
        )
        
        next_week_slot: Optional[str] = get_slot_value(
            handler_input=handler_input, slot_name="next_week"
        )
        is_next_week_slot = next_week_slot is not None

        requested_date = get_requested_day(resolved_day, is_next_week_slot)

        # get the dishes at the requested date
        dishes_at_date = [
            dish
            for dish in self.dishes
            if dish.day == requested_date
        ]

        # if list is empty it must be weekend or a holiday
        if not dishes_at_date:
            speech_output = f"{resolved_day} gibt es kein Essen in der Mensa. Die Mensa hat am Wochenende und an Feiertagen geschlossen."
        else:
            speech_output = get_list_speech_output(dishes_at_date)

        handler_input.response_builder.speak(speech_output)
        return handler_input.response_builder.response

    # set dishes - called by base_builder
    def set_dishes(self, dishes: Sequence[Dish]) -> None:
        self.dishes = dishes


class DayAndCategoryIntentHandler(AbstractRequestHandler):

    dishes: Sequence[Dish]

    def can_handle(self, handler_input: HandlerInput) -> bool:
        return is_intent_name("DayAndCategoryIntent")(handler_input)

    def handle(self, handler_input: HandlerInput) -> Response:
        
        # get slot value
        day_slot = get_slot(handler_input=handler_input, slot_name="day")
        resolved_day = get_resolved_slot_value(
            slot=day_slot, resolution_authority_name="TAG"
        )

        next_week_slot: Optional[str] = get_slot_value(
            handler_input=handler_input, slot_name="next_week"
        )
        is_next_week_slot = next_week_slot is not None

        category_slot = get_slot(handler_input=handler_input, slot_name="category")
        resolved_category = get_resolved_slot_value(
            slot=category_slot, resolution_authority_name="KATEGORIE"
        )

        requested_date = get_requested_day(resolved_day, is_next_week_slot)

        dishes_for_category_and_date = [
            dish
            for dish in self.dishes
            if dish.day == requested_date and dish.category == resolved_category
        ]

        if not dishes_for_category_and_date:
            speech_output = f"{resolved_day} gibt es kein Essen in der Mensa. Die Mensa hat am Wochenende und an Feiertagen geschlossen."
        else:
            speech_output = get_list_speech_output(dishes_for_category_and_date)

        handler_input.response_builder.speak(speech_output)
        return handler_input.response_builder.response

    def set_dishes(self, dishes: Sequence[Dish]):
        self.dishes = dishes
