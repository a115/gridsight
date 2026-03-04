import random
from datetime import UTC, datetime
from decimal import Decimal
from enum import StrEnum
from typing import Protocol

from django.utils import timezone
from pydantic import BaseModel

from etl.models import Plant, TimeSeriesData
from utils import get_start_and_end_of_settlement_period


class FuelType(StrEnum):
    COAL = "coal"
    GAS = "gas"


class BalancingDirection(StrEnum):
    UP = "up"
    DOWN = "down"


class PlantState(StrEnum):
    GENERATING = "GENERATING"
    STANDBY = "STANDBY"
    BALANCING = "BALANCING"
    ACCEPTED_BID = "ACCEPTED_BID"
    TRIP = "TRIP"
    OUTAGE = "OUTAGE"


class PlantStatus(BaseModel): ...


class PlantCoreStatus(PlantStatus):
    """
    The core status of a `Plant` object. These attributes are always
    defined regardless of the full status of the plant.
    """

    name: str
    state: PlantState
    mel: Decimal
    fpn: Decimal


class PlantBalancingStatus(PlantStatus):
    """
    The components of the status that are defined only if the
    plant is in `BALANCING` state.
    """

    balancing_direction: BalancingDirection


class PlantBidAcceptedStatus(PlantStatus):
    """
    The components of the status that are defined only if the
    plant is in `ACCEPTED_BID` state.
    """

    offer_price: Decimal
    start_time: datetime


class PlantFullStatus(BaseModel):
    """
    A container class that allows segregating mutually exclusive
    parts of the status.
    """

    core_status: PlantCoreStatus
    balancing_status: PlantBalancingStatus | None = None
    bid_accepted_status: PlantBidAcceptedStatus | None = None


class PlantStateVariables(BaseModel):
    previous_mel: Decimal
    current_mel: Decimal
    current_fpn: Decimal
    last_boa_volume: Decimal | None


class PlantStateRule(Protocol):
    """
    An interface for a function that determines the state of a plant based on the given variables.
    """

    def __call__(self, variables: PlantStateVariables) -> PlantState | None: ...


class PlantStateSolver:
    def __init__(self):
        self.state_rules = [
            PlantStateSolver.check_for_trip_or_outage,
            PlantStateSolver.check_if_generating_or_balancing,
            PlantStateSolver.check_if_accepted_bid_or_standby,
        ]
        self.default_state = PlantState.STANDBY

    @staticmethod
    def check_for_trip_or_outage(
        variables: PlantStateVariables,
    ) -> PlantState | None:
        # 1. Handle critical offline states first, as they override everything.
        if variables.current_mel == 0:
            # This was a sudden drop while planned to be running.
            if variables.previous_mel > 0 and variables.current_fpn > 0:
                return PlantState.TRIP
            # It's unavailable with no recent change; a planned or long-term outage.
            else:
                return PlantState.OUTAGE
        return None

    @staticmethod
    def check_if_generating_or_balancing(
        variables: PlantStateVariables,
    ) -> PlantState | None:
        # 2. Check for active generation vs. balancing using the FPN and BOA volume
        if variables.current_fpn > 0 and not variables.last_boa_volume:
            return PlantState.GENERATING
        if variables.last_boa_volume:
            return PlantState.BALANCING

    @staticmethod
    def check_if_accepted_bid_or_standby(
        variables: PlantStateVariables,
    ) -> PlantState | None:
        # 3. If we get here, the plant is NOT generating. Now determine why.
        # TODO: Implement logic to determine if a plant has an accepted bid
        has_accepted_bid = random.choice([True, False])

        # It's offline but has a contract to start soon.
        if has_accepted_bid:
            return PlantState.ACCEPTED_BID
        # It's available, not planned to run, and has no upcoming bids. Classic standby.
        if variables.current_fpn == 0 and variables.current_mel > 0:
            return PlantState.STANDBY

    def resolve_state(
        self,
        variables: PlantStateVariables,
    ) -> PlantState:
        for rule in self.state_rules:
            state = rule(variables)
            if state is not None:
                return state
        return self.default_state


class PlantStatusSolver:
    @staticmethod
    def resolve_state(
        variables: PlantStateVariables,
    ) -> PlantState:
        return PlantStateSolver().resolve_state(variables=variables)

    @staticmethod
    def resolve_balancing_direction(
        state: PlantState,
        last_boa_volume: Decimal | None,
    ) -> BalancingDirection | None:
        if not last_boa_volume:
            return

        if state == PlantState.BALANCING:
            if last_boa_volume > 0:
                return BalancingDirection.UP
            else:
                return BalancingDirection.DOWN

    @staticmethod
    def resolve_fpn(
        plant: Plant,
    ) -> Decimal:
        # TODO: Implement actual FPN resolution logic
        fpn = (
            TimeSeriesData.objects.filter(metric_id=2, plant=plant)
            .order_by("-time")
            .values_list("value", flat=True)
            .first()
            or 0
        )

        return Decimal(fpn)

    @staticmethod
    def last_two_mels(
        plant: Plant,
    ) -> list[Decimal]:
        mel = TimeSeriesData.objects.filter(metric_id=1, plant=plant).order_by(
            "-time"
        ).values_list("value", flat=True)[:2] or [0, 0]

        return [Decimal(mel[0]), Decimal(mel[1])]

    @staticmethod
    def boa_volume_for_current_settlement_period(plant: Plant) -> Decimal | None:
        """
        Returns the BOA volume for the current settlement period for the given plant.

        The acceptance of a bid or offer is an event but the data is stored
        as a time-series record in this version.
        """
        now = timezone.now()
        start, end = get_start_and_end_of_settlement_period(now)

        boa_volume = (
            TimeSeriesData.objects.filter(metric_id=5, plant=plant)
            .filter(time__range=(start, end))
            .order_by("-time")
            .values_list("value", flat=True)
            .first()
        )

        if boa_volume:
            return Decimal(boa_volume)

    @staticmethod
    def resolve(
        plant: Plant,
    ) -> PlantFullStatus:
        last_two_mels = PlantStatusSolver.last_two_mels(plant=plant)
        current_mel = last_two_mels[0]
        previous_mel = last_two_mels[1]

        current_fpn = PlantStatusSolver.resolve_fpn(plant=plant)
        last_boa_volume = PlantStatusSolver.boa_volume_for_current_settlement_period(
            plant=plant
        )
        state = PlantStatusSolver.resolve_state(
            variables=PlantStateVariables(
                current_mel=current_mel,
                previous_mel=previous_mel,
                current_fpn=current_fpn,
                last_boa_volume=last_boa_volume,
            )
        )
        balancing_direction = PlantStatusSolver.resolve_balancing_direction(
            state=state,
            last_boa_volume=last_boa_volume,
        )

        bid_accepted_status = None
        if state == PlantState.ACCEPTED_BID:
            # TODO: Implement me
            bid_accepted_status = PlantBidAcceptedStatus(
                offer_price=Decimal(100.5),
                start_time=datetime.now(tz=UTC),
            )

        balancing_status = None
        if balancing_direction:
            balancing_status = PlantBalancingStatus(
                balancing_direction=balancing_direction,
            )

        core_status = PlantCoreStatus(
            name=str(plant.name),
            state=state,
            fpn=current_fpn,
            mel=current_mel,
        )

        return PlantFullStatus(
            core_status=core_status,
            balancing_status=balancing_status,
            bid_accepted_status=bid_accepted_status,
        )
