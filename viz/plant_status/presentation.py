from enum import StrEnum
from datetime import datetime

from pydantic import BaseModel
from viz.plant_status.status import PlantFullStatus

from etl.models import Plant
from viz.plant_status.status import PlantStatusSolver


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
    # Card status
    status_class: StatusClass
    badge_class: BadgeClass
    status_text: StatusText
    icon: str | None = None

    # Domain-specific plant status
    plant_status: PlantFullStatus


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
            StatusClass.STANDBY: BadgeClass.SUCCESS,
            StatusClass.BALANCING: BadgeClass.WARNING,
            StatusClass.ACCEPTED_BID: BadgeClass.INFO,
            StatusClass.TRIP: BadgeClass.DANGER,
            StatusClass.OUTAGE: BadgeClass.SECONDARY,
        }
        return _badge_class_map.get(status_class, BadgeClass.WARNING)

    @staticmethod
    def resolve(
        plant: Plant,
    ) -> PlantStatusCard:
        plant_status = PlantStatusSolver.resolve(plant)
        plant_state_value = plant_status.core_status.state.value
        plant_status_class = StatusClass[plant_status.core_status.state.value]

        return PlantStatusCard(
            status_class=plant_status_class,
            badge_class=PlantStatusCardResolver._resolve_badge_class(
                plant_status_class
            ),
            status_text=StatusText[plant_state_value],
            icon=None,
            plant_status=plant_status,
        )
