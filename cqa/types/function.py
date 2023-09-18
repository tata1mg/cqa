from dataclasses import dataclass, field
from typing import List


@dataclass
class Function:
    name: str
    return_type: type = field(default=None)
    args: List[type] = field(default_factory=list)
