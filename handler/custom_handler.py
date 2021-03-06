from datetime import datetime
from typing import Dict, List, Optional

from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.utils import get_slot, is_intent_name
from ask_sdk_model import Response, Slot
from ask_sdk_model.slu.entityresolution import Value

import handler.speech_output as speech_output
from handler.context import Context
from handler.dish import Dish

sb = SkillBuilder()
context = Context()


# pylint: disable=too-many-nested-blocks
def _resolve_slots(handler_input: HandlerInput, slot_names: List[str]) -> Dict[str, str]:
    resolved: Dict[str, str] = {}
    slot_value: Optional[Slot]
    for slot_name in slot_names:
        # if slot not exists, None is returned by get_slot()
        slot_value = get_slot(handler_input, slot_name)
        if slot_value is None:
            resolved[slot_name] = ""
        assert slot_value is not None

        # resolutions exists for custom slot types and extended standard slot types
        # authority is the name of the defined slot type
        slot_resolutions = slot_value.resolutions
        if slot_resolutions is not None:
            for resolution_authority in slot_resolutions.resolutions_per_authority:  # type: ignore
                if resolution_authority.authority == slot_name:
                    res_value = resolution_authority.values[0].value  # type: ignore
                    if isinstance(res_value, Value):
                        if isinstance(res_value.name, str):
                            resolved[slot_name] = res_value.name
                    else:
                        resolved[slot_name] = ""
                    break
            else:
                resolved[slot_name] = slot_value.value or ""
        else:
            resolved[slot_name] = slot_value.value or ""
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
    def can_handle(self, handler_input: HandlerInput) -> bool:
        return is_intent_name("DayIntent")(handler_input)

    def handle(self, handler_input: HandlerInput) -> Response:
        resolved_slot_values = _resolve_slots(handler_input, ["day"])
        requested_date = datetime.strptime(resolved_slot_values["day"], "%Y-%m-%d")
        dishes_at_date = [dish for dish in context.dishes if dish.day == requested_date.date()]
        if not dishes_at_date:
            sorted_dishes = _sort_dishes_by_category(dishes_at_date)
            output = speech_output.speak_categories(sorted_dishes)
        else:
            output = speech_output.no_dishes_found_at_date(requested_date)
        handler_input.response_builder.speak(output)
        return handler_input.response_builder.response


class DayAndCategoryIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input: HandlerInput) -> bool:
        return is_intent_name("DayAndCategoryIntent")(handler_input)

    def handle(self, handler_input: HandlerInput) -> Response:
        resolved_slot_values = _resolve_slots(handler_input, ["day", "category"])
        requested_date = datetime.strptime(resolved_slot_values["day"], "%Y-%m-%d")
        requested_category = resolved_slot_values["category"]

        dishes_for_category_and_date = [
            dish
            for dish in context.dishes
            if dish.day == requested_date.date() and dish.category == requested_category
        ]
        if not dishes_for_category_and_date:
            output = speech_output.no_dishes_found_in_category(requested_date, requested_category)
        else:
            output = speech_output.speak_categories(
                {requested_category: dishes_for_category_and_date}
            )

        handler_input.response_builder.speak(output)
        return handler_input.response_builder.response
