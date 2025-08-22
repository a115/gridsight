from datetime import datetime, timezone
from django.shortcuts import render
from viz.data_models.plant_status import (
    PlantStatusCard,
    StatusClass,
    StatusText,
    BadgeClass,
    BalancingDirection,
    PlantStatusViewContext,
)


def plant_status_board_view(request):
    """
    View to render the Live Plant Status Board.
    """

    search_query = request.GET.get("search", "")
    fuel_filter = request.GET.get("fuel_type", "all")
    sort_filter = request.GET.get("sort", "mel")

    # This data will eventually come from live database queries.
    plants_data = [
        PlantStatusCard(
            name="T_DRAX-1",
            status_class=StatusClass.GENERATING,
            badge_class=BadgeClass.PRIMARY,
            status_text=StatusText.GENERATING,
            icon=None,
            actual_gen=640,
            fpn=640,
            mel=645,
            balancing_direction=None,
        ),
        PlantStatusCard(
            name="T_PEMB-21",
            status_class=StatusClass.BALANCING,
            badge_class=BadgeClass.WARNING,
            status_text=StatusText.BALANCING,
            icon=None,
            actual_gen=450,
            fpn=400,
            mel=510,
            balancing_direction=BalancingDirection.UP,
        ),
        PlantStatusCard(
            name="T_STAY-1",
            status_class=StatusClass.STANDBY,
            badge_class=BadgeClass.SUCCESS,
            status_text=StatusText.STANDBY,
            icon=None,
            actual_gen=0,
            fpn=0,
            mel=350,
            balancing_direction=None,
        ),
        PlantStatusCard(
            name="T_WBURB-1",
            status_class=StatusClass.TRIP,
            badge_class=BadgeClass.DANGER,
            status_text=StatusText.TRIP,
            icon="bi-exclamation-triangle-fill",
            actual_gen=0,
            fpn=450,
            mel=0,
            balancing_direction=None,
        ),
        PlantStatusCard(
            name="T_EGGPS-1",
            status_class=StatusClass.OUTAGE,
            badge_class=BadgeClass.SECONDARY,
            status_text=StatusText.OUTAGE,
            icon=None,
            actual_gen=0,
            fpn=0,
            mel=0,
            balancing_direction=None,
        ),
        PlantStatusCard(
            name="T_GRAIN-1",
            status_class=StatusClass.GENERATING,
            badge_class=BadgeClass.PRIMARY,
            status_text=StatusText.GENERATING,
            icon=None,
            actual_gen=420,
            fpn=420,
            mel=420,
            balancing_direction=None,
        ),
        PlantStatusCard(
            name="T_CORBY-1",
            status_class=StatusClass.STANDBY,
            badge_class=BadgeClass.SUCCESS,
            status_text=StatusText.STANDBY,
            icon=None,
            actual_gen=0,
            fpn=0,
            mel=180,
            balancing_direction=None,
        ),
        PlantStatusCard(
            name="T_HARTL-1",
            status_class=StatusClass.GENERATING,
            badge_class=BadgeClass.PRIMARY,
            status_text=StatusText.GENERATING,
            icon=None,
            actual_gen=595,
            fpn=595,
            mel=595,
            balancing_direction=None,
        ),
        # This next one represents a plant in the "Accepted Bid" state and requires new keys: offer_price and start_time
        PlantStatusCard(
            name="T_FFES-4",
            status_class=StatusClass.ACCEPTED_BID,
            badge_class=BadgeClass.INFO,
            status_text=StatusText.ACCEPTED_BID,
            icon="bi-hourglass-split",
            actual_gen=0,
            fpn=0,
            mel=60,
            balancing_direction=None,
            offer_price=115,
            start_time="19:00",
        ),
    ]
    current_datetime = datetime.now(timezone.utc)
    context = PlantStatusViewContext(
        plants=plants_data,
        search_query=search_query,
        fuel_filter=fuel_filter,
        sort_filter=sort_filter,
        last_refreshed=current_datetime,
    )
    return render(
        request,
        "plant_status_board.html",
        context.model_dump(),
    )
