from datetime import datetime
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.dispatch_components import AbstractRequestHandler, AbstractExceptionHandler
from ask_sdk_model import Response
from ask_sdk_model.ui import SimpleCard


class LaunchRequestHandler(AbstractRequestHandler):
    @staticmethod
    def get_greeting() -> str:
        current_hour = datetime.now().time().hour
        if current_hour <= 4 or current_hour >= 21:
            return "Gute Nacht."
        if 4 <= current_hour < 10:
            return "Guten Morgen."
        if 10 <= current_hour < 18:
            return "Guten Tag."
        return "Guten Abend"

    def can_handle(self, handler_input: HandlerInput) -> bool:
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input: HandlerInput) -> Response:
        greeting = (
            f" {self.get_greeting} Möchtest du wissen, was es in der Mensa Mittweida gibt?"
            " Sage dazu zum Beispiel: Was gibt es am Montag in der Mensa."
            " Wenn du weitere Hilfe brauchst sage: Hilfe"
        )
        handler_input.response_builder.speak(greeting).set_card(SimpleCard("Wilkommen", greeting))
        return handler_input.response_builder.response


class HelpIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input: HandlerInput) -> bool:
        return is_intent_name("Amazon.HelpIntent")(handler_input)

    def handle(self, handler_input: HandlerInput) -> Response:
        help_message = (
            "Wenn du wissen möchtest, welche Gerichte es an einem bestimmten Tag gibt, "
            "sage z.B. was gibt es am Montag. Wenn du ein bestimmtes Gericht wissen "
            "möchtest, sage: Was ist der Campusteller am Dienstag. Interessieren dich "
            "die Zusatzstoffe, kannst du mich fragen: Welche Zusatzstoffe hat der "
            "Campusteller am Dienstag zum beenden sage: beenden"
        )
        handler_input.response_builder.speak(help_message).set_card(
            SimpleCard("Hilfe", help_message)
        )
        return handler_input.response_builder.response


class ExitIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input: HandlerInput) -> bool:
        return is_intent_name("AMAZON.CancelIntent")(handler_input) or is_intent_name(
            "AMAZON.StopIntent"
        )(handler_input)

    def handle(self, handler_input: HandlerInput) -> Response:
        handler_input.response_builder.speak("Auf Wiedersehen").set_card(
            SimpleCard("Auf Wiedersehen")
        )
        return handler_input.response_builder.response


class SessionEndedRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input: HandlerInput) -> bool:
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input: HandlerInput) -> Response:
        return handler_input.response_builder.response


class CatchAllExceptionHandler(AbstractExceptionHandler):
    def can_handle(self, handler_input: HandlerInput, exception: Exception) -> bool:
        return True

    def handle(self, handler_input: HandlerInput, exception: Exception) -> Response:
        speech = "Ich habe leider nicht verstanden, was du gesagt hast."
        handler_input.response_builder.speak(speech).ask(speech)
        return handler_input.response_builder.response
