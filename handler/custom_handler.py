from ask_sdk_core.utils import is_intent_name, get_slot_value
from ask_sdk_model.ui import SimpleCard
from ask_sdk_core.skill_builder import SkillBuilder

sb = SkillBuilder()


@sb.request_handler(can_handle_func=is_intent_name("DayIntent"))
def day_intent_handler(handler_input):

    #get slot value
    day = get_slot_value(
        handler_input=handler_input, slot_name="day")