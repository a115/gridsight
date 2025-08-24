import random
from enum import StrEnum
from viz.plant_status.data_models import (
    BalancingDirection,
)
from decimal import Decimal
from pydantic import BaseModel
from etl.models import Plant


class PlantState(StrEnum):
    GENERATING = "GENERATING"
    STANDBY = "STANDBY"
    BALANCING = "BALANCING"
    ACCEPTED_BID = "ACCEPTED_BID"
    TRIP = "TRIP"
    OUTAGE = "OUTAGE"


class PlantStatus(BaseModel):
    name: str
    state: PlantState
    fpn: Decimal
    mel: Decimal
    current_generation: Decimal
    balancing_direction: BalancingDirection


class PlantStatusSolver:
    @staticmethod
    def resolve_state(
        plant: Plant,
    ) -> PlantState:
        # TODO: Implement actual state resolution logic
        return random.choice(list(PlantState))

    @staticmethod
    def resolve_balancing_direction(
        plant: Plant,
    ) -> BalancingDirection:
        # TODO: Implement actual balancing direction resolution logic
        return random.choice(list(BalancingDirection))

    @staticmethod
    def resolve_current_generation(
        plant: Plant,
    ) -> Decimal:
        # TODO: Implement actual current generation resolution logic
        return Decimal(random.randrange(0, int(plant.generation_capacity)))

    @staticmethod
    def resolve_fpn(
        plant: Plant,
    ) -> Decimal:
        # TODO: Implement actual FPN resolution logic
        return Decimal(random.randrange(0, int(plant.generation_capacity)))

    @staticmethod
    def resolve_mel(
        plant: Plant,
    ) -> Decimal:
        # TODO: Implement actual MEL resolution logic
        return Decimal(random.randrange(0, int(plant.generation_capacity)))

    @staticmethod
    def resolve(
        plant: Plant,
    ) -> PlantStatus:
        return PlantStatus(
            name=plant.name,
            state=PlantStatusSolver.resolve_state(plant),
            fpn=PlantStatusSolver.resolve_fpn(plant),
            mel=PlantStatusSolver.resolve_mel(plant),
            current_generation=PlantStatusSolver.resolve_current_generation(plant),
            balancing_direction=PlantStatusSolver.resolve_balancing_direction(plant),
        )
