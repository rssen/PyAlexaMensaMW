from datetime import datetime

from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_model import Response
from ask_sdk_model.ui import SimpleCard

sb = SkillBuilder()


@sb.request_handler(can_handle_func=is_request_type("LaunchRequest"))
def launch_request_handler(handler_input: HandlerInput) -> Response:
    def get_greeting() -> str:
        current_hour = datetime.now().time().hour
        if current_hour <= 4 or current_hour >= 21:
            return "Gute Nacht."
        elif 4 <= current_hour < 10:
            return "Guten Morgen."
        elif 10 <= current_hour < 18:
            return "Guten Tag."
        else:
            return "Guten Abend"

    greeting = f" {get_greeting} Möchtest du wissen, was es in der Mensa Mittweida gibt?" \
               " Sage dazu zum Beispiel: Was gibt es am Montag in der Mensa." \
               " Wenn du weitere Hilfe brauchst sage: Hilfe"
    handler_input.response_builder.speak(greeting).set_card(SimpleCard("Wilkommen", greeting))

    return handler_input.response_builder.response


@sb.request_handler(can_handle_func=is_intent_name("Amazon.HelpIntent"))
def help_intent_handler(handler_input: HandlerInput) -> Response:
    help_message = \
        ("Wenn du wissen möchtest, welche Gerichte es an einem bestimmten Tag gibt, "
         "sage z.B. was gibt es am Montag. Wenn du ein bestimmtes Gericht wissen "
         "möchtest, sage: Was ist der Campusteller am Dienstag. Interessieren dich "
         "die Zusatzstoffe, kannst du mich fragen: Welche Zusatzstoffe hat der "
         "Campusteller am Dienstag zum beenden sage: beenden")
    handler_input.response_builder.speak(help_message).set_card(SimpleCard("Hilfe", help_message))
    return handler_input.response_builder.response


@sb.request_handler(
    can_handle_func=lambda handler_input:
    is_intent_name("AMAZON.CancelIntent")(handler_input) or
    is_intent_name("AMAZON.StopIntent")(handler_input))
def cancel_and_stop_intent_handler(handler_input: HandlerInput) -> Response:
    return handler_input.response_builder.speak("Auf Wiedersehen").set_card(
        SimpleCard("Auf Wiedersehen")).response


@sb.request_handler(can_handle_func=is_request_type("SessionEndedRequest"))
def session_ended_request_handler(handler_input: HandlerInput) -> Response:
    return handler_input.response_builder.response


@sb.exception_handler(can_handle_func=lambda i, e: True)
def all_exception_handler(handler_input: HandlerInput, exception: Exception) -> Response:
    # Log the exception in CloudWatch Logs
    print(exception)
    speech = "Ich habe leider nicht verstanden, was du gesagt hast."
    handler_input.response_builder.speak(speech).ask(speech)
    return handler_input.response_builder.response
