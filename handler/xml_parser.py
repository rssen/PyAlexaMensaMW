from dataclasses import dataclass
from typing import Sequence, Tuple, Mapping, List, Dict
from datetime import datetime
from xml.sax import SAXParseException
from untangle import parse


def parse_xml(url: str) -> Sequence["Dish"]:
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

    dishes: List[Dish] = []
    try:
        doc = parse(url)
    except (AttributeError, ValueError, SAXParseException) as e:
        raise AttributeError(f"could not parse url {url}: {e}")

    for day in doc.response.menus.day:
        for menu in day.menu:
            k: Dict[str, str] = {
                name: menu.get_elements(name)[0].cdata
                for name in dir(menu)
                if name not in ["prices"]
            }
            dishes.append(
                Dish(
                    datetime.strptime(day.date.cdata, "%Y-%m-%d").date(),
                    k.get("type", ""),
                    k.get("description", ""),
                    k.get("pc", ""),
                    k.get("available") == "true",
                    {key: (val == "true") for (key, val) in k.items() if key in ingredients},
                    tuple(k.get("additives", "").split(",")),  # type: ignore
                    [
                        Dish.Price(
                            price.category.cdata,
                            float((price.value.cdata).replace(",", ".")),
                            price.label.cdata,
                        )
                        for price in menu.prices.price
                    ],
                )
            )
    return dishes


@dataclass
class Dish:
    # pylint: disable=too-many-instance-attributes
    day: datetime.date
    category: str
    description: str
    price_category: str
    available: bool
    ingredients: Mapping[str, bool]
    additives: Tuple[str]
    prices: Sequence["Dish.Price"]

    @dataclass
    class Price:
        category: str
        value: float
        label: str
