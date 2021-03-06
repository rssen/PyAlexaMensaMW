from datetime import datetime
from typing import Dict, List

from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.utils import get_slot, is_intent_name
from ask_sdk_model import Response, Slot

import handler.speech_output as speech_output
from handler.context import Context
from handler.dish import Dish

sb = SkillBuilder()
context = Context()


def _resolve_slots(handler_input: HandlerInput, slot_names: List[str]) -> Dict[str, str]:
    resolved: Dict[str, str] = {}
    slot_value: Slot
    for slot_name in slot_names:
        # if slot not exists, None is returned by get_slot()
        slot_value = get_slot(handler_input, slot_name)
        if slot_value is None:
            resolved[slot_name] = ""

        # resolutions exists for custom slot types and extended standard slot types
        # authority is the name of the defined slot type
        slot_resolutions = slot_value.resolutions
        if slot_resolutions is not None:
            for resolution_authority in slot_resolutions.resolutions_per_authority:
                if resolution_authority.authority == slot_name:
                    resolved[slot_name] = resolution_authority.values[0].value.name
                    break
            else:
                resolved[slot_name] = slot_value.value
        else:
            resolved[slot_name] = slot_value.value
    return resolved


def _sort_dishes_by_category(dishes: List[Dish]) -> Dict[str, List[Dish]]:
    categories: Dict[str, List[Dish]] = {}
    for dish in dishes:
        if dish.category not in categories.keys():
            categories[dish.category] = [dish]
        else:
            categories[dish.category].append(dish)
    return categories


class DayIntentHandler(AbstractRequestHandler):
    def __init__(self):
        self.dishes_at_date: List[Dish] = []

    def can_handle(self, handler_input: HandlerInput) -> bool:
        return is_intent_name("DayIntent")(handler_input)

    def handle(self, handler_input: HandlerInput) -> Response:
        resolved_slot_values = _resolve_slots(handler_input, ["day"])
        requested_date = datetime.strptime(resolved_slot_values["day"], "%Y-%m-%d")
        self.dishes_at_date = [dish for dish in context.dishes if dish.day == requested_date.date()]
        sorted_dishes = _sort_dishes_by_category(self.dishes_at_date)
        output = speech_output.speak_categories(sorted_dishes)
        print(output)
        handler_input.response_builder.speak(output)
        return handler_input.response_builder.response


"""class DayAndCategoryIntentHandler(AbstractRequestHandler):

    dishes: Sequence[Dish]

    def can_handle(self, handler_input: HandlerInput) -> bool:
        return is_intent_name("DayAndCategoryIntent")(handler_input)

    def handle(self, handler_input: HandlerInput) -> Response:

        # get slot value
        day_slot = get_slot(handler_input=handler_input, slot_name="day")
        resolved_day = get_slot(slot=day_slot, resolution_authority_name="TAG")

        next_week_slot: Optional[str] = get_slot_value(
            handler_input=handler_input, slot_name="next_week"
        )
        is_next_week_slot = next_week_slot is not None

        category_slot = get_slot(handler_input=handler_input, slot_name="category")
        resolved_category = __get_resolved_slot_value(
            slot=category_slot, resolution_authority_name="KATEGORIE"
        )

        requested_date = get_date(resolved_day, is_next_week_slot)

        dishes_for_category_and_date = [
            dish
            for dish in self.dishes
            if dish.day == requested_date and dish.category == resolved_category
        ]

        if not dishes_for_category_and_date:
            speech_output = (
                f"{resolved_day} gibt es kein Essen in der Mensa. "
                f"Die Mensa hat am Wochenende und an Feiertagen geschlossen."
            )
        else:
            speech_output = get_list_speech_output(dishes_for_category_and_date)

        handler_input.response_builder.speak(speech_output)
        return handler_input.response_builder.response

    def set_dishes(self, dishes: Sequence[Dish]):
        self.dishes = dishes"""
