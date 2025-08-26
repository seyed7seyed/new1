# api/schemas.py
from pydantic import BaseModel, HttpUrl, root_validator
from typing   import List

# Sum
class SumInput(BaseModel):
    y: List[float]

# Plot
class PlotInput(BaseModel):
    x: List[float]
    y: List[float]

    @root_validator
    def check_lengths(cls, values):
        x, y = values.get("x"), values.get("y")
        if len(x) != len(y):
            raise ValueError("x and y must be the same length")
        return values

# Fetch Url
class URLInput(BaseModel):
    url: HttpUrl

# Enter by Hand
class TextInput(BaseModel):
    text: str
