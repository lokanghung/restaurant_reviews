from dataclasses import dataclass
from typing import Optional, List
from datetime import date




@dataclass
class AddReview:
    restaurant_id: int
    rating: int
    comment: Optional[str]

# @dataclass
# class UpdateProduct:
#     name: str
#     price: int
