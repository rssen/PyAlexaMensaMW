from ask_sdk_core.skill_builder import SkillBuilder
from handler.standard_handler import (
    SessionEndedRequestHandler,
    ExitIntentHandler,
    HelpIntentHandler,
    LaunchRequestHandler,
    CatchAllExceptionHandler,
)
from handler.custom_handler import DayIntentHandler
from handler.xml_parser import parse_xml

sb = SkillBuilder()
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(ExitIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(LaunchRequestHandler())
sb.add_exception_handler(CatchAllExceptionHandler())

# custom handler
dishes = parse_xml("https://app.hs-mittweida.de/speiseplan/all")
assert len(dishes) > 0
assert dishes is not None
day_intent_handler = DayIntentHandler()
day_intent_handler.set_dishes(dishes)
sb.add_request_handler(day_intent_handler) # register DayIntentHandler


handler = sb.lambda_handler()
