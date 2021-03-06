from datetime import date
from typing import Dict, List

from handler.context import Context
from handler.dish import Dish
from handler.template import template_factory

context = Context()
templates = template_factory(context.localization.value)


def no_dishes_found_at_date(requested_date: date):
    templates.get_error_no_dishes_at_date().substitute(requested_date=requested_date)


def no_dishes_found_in_category(requested_date: date, category: str):
    templates.get_error_category_empty_at_date().substitute(
        category=category, requested_date=requested_date
    )


def speak_dish_list(dishes: List[Dish]) -> str:
    descriptions = [dish.description for dish in dishes]
    return __connect(descriptions)


def speak_categories(category_dishes: Dict[str, List[Dish]]) -> str:
    output_categories: List[str] = []
    for category_name, dishes in category_dishes.items():
        dishes_phrase = speak_dish_list(dishes)
        output = templates.get_category_phrase().substitute(
            category_name=category_name, dishes=dishes_phrase
        )
        output_categories.append(output)
    joined_output = str.join(" ", output_categories)
    return joined_output.replace("&", "und")


def __connect(phrases: List[str]) -> str:
    if len(phrases) < 2:
        return phrases[0] if len(phrases) == 1 else ""
    connection_phrase = templates.get_connection_phrase()
    if len(phrases) == 2:
        return connection_phrase.substitute(phrase_1=phrases[0], phrase_2=phrases[1])

    phrase_1 = phrases.pop()
    phrase_2 = __connect(phrases)
    return connection_phrase.substitute(phrase_1=phrase_1, phrase_2=phrase_2)
