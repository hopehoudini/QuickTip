from dataclasses import dataclass, asdict
from typing import List

@dataclass
class Prompt:
    id: str
    title: str
    content: str
    enabled: bool = True

    def to_dict(self): return asdict(self)
    @classmethod
    def from_dict(cls, data): return cls(str(data['id']), data['title'], data['content'], data.get('enabled', True))
