from dataclasses import dataclass
from datetime import datetime
from typing import Mapping, Sequence, Tuple


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
