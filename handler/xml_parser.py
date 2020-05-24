from untangle import parse
from typing import Sequence, Tuple, Union, Mapping, List
from datetime import date
from pprint import pprint


def parse_xml() -> Sequence["Dish"]:

    dishes: List["Dish"] = []  # empty list, add dishes

    doc = parse("https://app.hs-mittweida.de/speiseplan/all")
    days = doc.response.menus.day

    for day in doc.response.menus.day:
        date = day.date.cdata
        for menu in day.menu:
            category = menu.type.cdata
            description = menu.description.cdata
            price_category = menu.pc.cdata
            available = menu.available.cdata
            additives = tuple(menu.additives.cdata.split(","))
            ingredients = {
                "alcohol": menu.alcohol.cdata,
                "pork": menu.pork.cdata,
                "vital": menu.vital.cdata,
                "beef": menu.beef.cdata,
                "bio": menu.bio.cdata,
                "birds": menu.birds.cdata,
                "fish": menu.fish.cdata,
                "garlic": menu.garlic.cdata,
                "lamb": menu.lamb.cdata,
                "vegan": menu.vegan.cdata,
                "vegetarian": menu.vegetarian.cdata,
                "venison": menu.venison.cdata,
            }
            prices = []
            for price in menu.prices.price:
                prices.append(
                    Dish.Price(price.category.cdata, price.value.cdata, price.label.cdata)
                )
            # data prepared, create dish object, add object to dishes list
            dishes.append(
                Dish(
                    date,
                    category,
                    description,
                    price_category,
                    available,
                    ingredients,
                    additives,
                    prices,
                )
            )

    return dishes


class Dish:
    def __init__(
        self,
        day: date,
        category: str,
        description: str,
        price_category: int,
        available: bool,
        ingredients: Mapping[str, bool],
        additives: Tuple[Union[str, int]],
        prices: Sequence["Dish.Price"],
    ):
        self._day = day
        self._category = category
        self._description = description
        self._price_category = price_category
        self._available = available
        self._ingredients = ingredients
        self._additives = additives
        self._prices = prices

    class Price:
        def __init__(self, category: str, value: float, label: str):
            self.category = category
            self.value = value
            self.label = label


if __name__ == "__main__":
    dishes = parse_xml()
    # import pprint
    for dish in dishes:
        pprint(vars(dish))
