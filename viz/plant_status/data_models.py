from enum import StrEnum


class FuelType(StrEnum):
    COAL = "coal"
    GAS = "gas"


class BalancingDirection(StrEnum):
    UP = "up"
    DOWN = "down"
