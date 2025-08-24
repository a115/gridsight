from enum import StrEnum
from pydantic import BaseModel
from decimal import Decimal
from datetime import datetime
from etl.models import Plant
from viz.plant_status.status import PlantStatusSolver

from viz.plant_status.data_models import (
    BalancingDirection,
)


class Card(BaseModel): ...


class BadgeClass(StrEnum):
    PRIMARY = "text-bg-primary"
    SECONDARY = "text-bg-secondary"
    SUCCESS = "text-bg-success"
    INFO = "text-bg-info"
    WARNING = "text-bg-warning"
    DANGER = "text-bg-danger"


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


class PlantStatusCardResolver:
    @staticmethod
    def _resolve_badge_class(
        status_class: StatusClass,
    ) -> BadgeClass:
        _badge_class_map = {
            StatusClass.GENERATING: BadgeClass.PRIMARY,
            StatusClass.STANDBY: BadgeClass.SECONDARY,
            StatusClass.ACCEPTED_BID: BadgeClass.SUCCESS,
            StatusClass.BALANCING: BadgeClass.INFO,
            StatusClass.TRIP: BadgeClass.DANGER,
            StatusClass.OUTAGE: BadgeClass.DANGER,
        }
        return _badge_class_map.get(status_class, BadgeClass.WARNING)

    @staticmethod
    def resolve(
        plant: Plant,
    ) -> PlantStatusCard:
        plant_status = PlantStatusSolver.resolve(plant)
        return PlantStatusCard(
            name=plant.name,
            status_class=StatusClass[plant_status.state.value],
            badge_class=PlantStatusCardResolver._resolve_badge_class(
                StatusClass[plant_status.state.value]
            ),
            status_text=StatusText[plant_status.state.value],
            icon=None,
            fpn=plant_status.fpn,
            mel=plant_status.mel,
            balancing_direction=plant_status.balancing_direction,
            actual_gen=plant_status.current_generation,
        )
