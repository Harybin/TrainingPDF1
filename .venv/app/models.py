from pydantic import BaseModel
from typing import List

class Exercise(BaseModel):
    name: str
    duration: int
    muscle_groups: List[str]
