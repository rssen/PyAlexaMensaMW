from dataclasses import dataclass
from datetime import date
from typing import Mapping, Sequence, Tuple


@dataclass
class Dish:
    # pylint: disable=too-many-instance-attributes
    day: date
    category: str
    description: str
    price_category: str
    available: bool
    ingredients: Mapping[str, bool]
    additives: Tuple[str]
    prices: Sequence["Dish.Price"]

    def __post_init__(self) -> None:
        self.description = self.description[: self.description.index("(")]
        self.category = self.category.lower()
        self.category = self.category.replace("&", "und")

    @dataclass
    class Price:
        category: str
        value: float
        label: str
