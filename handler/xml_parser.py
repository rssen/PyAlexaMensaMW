from untangle import parse
from typing import Sequence, Tuple, Union, Mapping, List
from datetime import date


def parse_xml() -> Sequence["Dish"]:

    dishes: List["Dish"] = []  # empty list, add dishes

    doc = parse("https://app.hs-mittweida.de/speiseplan/all")
    days = doc.response.menus.day

    print(days)
    print("Robin's Mama ist cool!")
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
    parse_xml()
