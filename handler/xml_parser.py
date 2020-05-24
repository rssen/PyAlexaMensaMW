from typing import Sequence, Tuple, Mapping, List, Dict
from datetime import date
from pprint import pprint
from untangle import parse


def parse_xml() -> Sequence["Dish"]:
    ingredients = [
        "alcohol",
        "pork",
        "vital",
        "beef",
        "bio",
        "birds",
        "fish",
        "garlic",
        "lamb",
        "vegan",
        "vegetarian",
        "venison",
    ]

    dishes: List["Dish"] = []  # empty list, add dishes
    doc = parse("https://app.hs-mittweida.de/speiseplan/all")
    for day in doc.response.menus.day:
        for menu in day.menu:
            k: Dict[str, str] = {
                name: menu.get_elements(name)[0].cdata
                for name in dir(menu)
                if name not in ["prices"]
            }
            dishes.append(
                Dish(
                    day.date.cdata,
                    k.get("type", ""),
                    k.get("description", ""),
                    k.get("pc", ""),
                    k.get("available") == "true",
                    {key: (val == "true") for (key, val) in k.items() if key in ingredients},
                    tuple(k.get("additives").split(",")),
                    [
                        Dish.Price(price.category.cdata, price.value.cdata, price.label.cdata)
                        for price in menu.prices.price
                    ],
                )
            )
    return dishes


class Dish:
    # pylint: disable=too-many-instance-attributes
    # pylint: disable=too-many-arguments

    def __init__(
        self,
        day: date,
        category: str,
        description: str,
        price_category: str,
        available: bool,
        ingredients: Mapping[str, bool],
        additives: Tuple[str],
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
    d = parse_xml()
    for dish in d:
        pprint(vars(dish))
    print(len(d))
