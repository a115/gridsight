from decimal import Decimal
from pydantic import BaseModel
from enum import StrEnum
from datetime import datetime


class StatusClass(StrEnum):
    GENERATING = "status-generating"
    STANDBY = "status-standby"
    BALANCING = "status-balancing"
    ACCEPTED_BID = "status-accepted-bid"
    TRIP = "status-trip"
    OUTAGE = "status-outage"


class StatusText(StrEnum):
    GENERATING = "Generating"
    STANDBY = "Standby"
    BALANCING = "Balancing"
    ACCEPTED_BID = "Accepted Bid"
    TRIP = "Trip"
    OUTAGE = "Outage"


class BadgeClass(StrEnum):
    PRIMARY = "text-bg-primary"
    SECONDARY = "text-bg-secondary"
    SUCCESS = "text-bg-success"
    INFO = "text-bg-info"
    WARNING = "text-bg-warning"
    DANGER = "text-bg-danger"


class BalancingDirection(StrEnum):
    UP = "up"
    DOWN = "down"


class Card(BaseModel):
    ...


class PlantStatusCard(Card):
    name: str
    status_class: StatusClass
    badge_class: BadgeClass
    status_text: StatusText
    icon: str | None
    actual_gen: Decimal
    fpn: Decimal
    mel: Decimal
    balancing_direction: BalancingDirection | None


class PlantStatusViewContext(BaseModel):
    plants: list[PlantStatusCard]
    search_query: str
    fuel_filter: str
    sort_filter: str
    last_refreshed: datetime
