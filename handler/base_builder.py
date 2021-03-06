from ask_sdk_core.skill_builder import SkillBuilder

from handler.context import Context
from handler.custom_handler import DayIntentHandler, DayAndCategoryIntentHandler
from handler.standard_handler import (
    CatchAllExceptionHandler,
    ExitIntentHandler,
    HelpIntentHandler,
    LaunchRequestHandler,
    SessionEndedRequestHandler,
)

sb = SkillBuilder()
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(ExitIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(LaunchRequestHandler())
sb.add_exception_handler(CatchAllExceptionHandler())

# custom handler
context = Context("https://app.hs-mittweida.de/speiseplan/all")

day_intent_handler = DayIntentHandler()
day_and_category_intent_handler = DayAndCategoryIntentHandler()

sb.add_request_handler(day_intent_handler)
sb.add_request_handler(day_and_category_intent_handler)

handler = sb.lambda_handler()
