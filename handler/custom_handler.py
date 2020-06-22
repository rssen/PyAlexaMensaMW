from typing import List, Sequence
from datetime import datetime

from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.handler_input import HandlerInput

from handler.xml_parser import Dish
from ask_sdk_core.utils import is_intent_name, get_slot_value
from ask_sdk_core.skill_builder import SkillBuilder

sb = SkillBuilder()


class BaseHandler:
    def __init__(self, dishes: Sequence[Dish]):
        self._dishes = dishes


class DayIntentHandler(AbstractRequestHandler, BaseHandler):
    def __init__(self, dishes: Sequence[Dish]):
        super(AbstractRequestHandler, self).__init__()
        self._dishes = dishes
        #super(BaseHandler, self).__init__(dishes)

    def can_handle(self, handler_input: HandlerInput) -> bool:
        return is_intent_name("DayIntent")(handler_input)

    def handle(self, handler_input: HandlerInput):
        # get slot value
        day_slot = get_slot_value(handler_input=handler_input, slot_name="day")
        print(day_slot)

        day_name = ['montag', 'dienstag', 'mittwoch', 'donnerstag', 'freitag', 'samstag', 'sonntag']
        day_of_week = datetime.today().weekday()
        day_slot_number = day_name.index(day_slot)
