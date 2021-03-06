from enum import Enum


class SkillException(Exception):
    def __init__(self, message: str, severity: "Severity", location: "Location"):
        self.msg = f"error: severity->{severity.name.lower()} location->{location.name.lower()} msg->{message}"
        super().__init__(self.msg)

    def __str__(self) -> str:
        return self.msg


class Severity(Enum):
    FATAL = 1
    WARNING = 2


class Location(Enum):
    XML_PARSER = "xml-parser"
    OUTPUT_TEMPLATE = "template"
    DAY_INTENT_HANDLER = "day_intent_handler"

