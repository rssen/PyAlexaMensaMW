from ask_sdk_core.skill_builder import SkillBuilder
from handler.standard_handler import (
    SessionEndedRequestHandler,
    ExitIntentHandler,
    HelpIntentHandler,
    LaunchRequestHandler,
    CatchAllExceptionHandler,
)

sb = SkillBuilder()
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(ExitIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(LaunchRequestHandler())

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()
