from __future__ import annotations

# python built-in imports
from dataclasses import dataclass, field
from datetime import date


@dataclass
class Show:
    id: str
    type: str
    title: str
    director: str | None
    cast: str | None
    country: str | None
    date_added: date | None
    release_year: int
    duration: str
    listed_in: str
    description: str
    rating: str | None = field(default=None)
