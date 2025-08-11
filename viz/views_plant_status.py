from datetime import datetime, timezone
from django.shortcuts import render


def plant_status_board_view(request):
    """
    View to render the Live Plant Status Board.
    """

    search_query = request.GET.get("search", "")
    fuel_filter = request.GET.get("fuel_type", "all")
    sort_filter = request.GET.get("sort", "mel")

    # This data will eventually come from live database queries.
    plants_data = [
        {
            "name": "T_DRAXX-1",
            "status_class": "status-generating",
            "badge_class": "text-bg-primary",
            "status_text": "Generating",
            "icon": None,
            "actual_gen": 640,
            "fpn": 640,
            "mel": 645,
            "balancing_direction": None,
        },
        {
            "name": "T_PEMB-21",
            "status_class": "status-balancing",
            "badge_class": "text-bg-warning",
            "status_text": "Balancing",
            "icon": None,
            "actual_gen": 450,
            "fpn": 400,
            "mel": 510,
            "balancing_direction": "up",
        },
        {
            "name": "T_STAY-1",
            "status_class": "status-standby",
            "badge_class": "text-bg-success",
            "status_text": "Standby",
            "icon": None,
            "actual_gen": 0,
            "fpn": 0,
            "mel": 350,
            "balancing_direction": None,
        },
        {
            "name": "T_WBURB-1",
            "status_class": "status-trip",
            "badge_class": "text-bg-danger",
            "status_text": "Trip",
            "icon": "bi-exclamation-triangle-fill",
            "actual_gen": 0,
            "fpn": 450,
            "mel": 0,
            "balancing_direction": None,
        },
        {
            "name": "T_EGGPS-1",
            "status_class": "status-outage",
            "badge_class": "text-bg-secondary",
            "status_text": "Outage",
            "icon": None,
            "actual_gen": 0,
            "fpn": 0,
            "mel": 0,
            "balancing_direction": None,
        },
        {
            "name": "T_GRAIN-1",
            "status_class": "status-generating",
            "badge_class": "text-bg-primary",
            "status_text": "Generating",
            "icon": None,
            "actual_gen": 420,
            "fpn": 420,
            "mel": 420,
            "balancing_direction": None,
        },
        {
            "name": "T_CORBY-1",
            "status_class": "status-standby",
            "badge_class": "text-bg-success",
            "status_text": "Standby",
            "icon": None,
            "actual_gen": 0,
            "fpn": 0,
            "mel": 180,
            "balancing_direction": None,
        },
        {
            "name": "T_HARTL-1",
            "status_class": "status-generating",
            "badge_class": "text-bg-primary",
            "status_text": "Generating",
            "icon": None,
            "actual_gen": 595,
            "fpn": 595,
            "mel": 595,
            "balancing_direction": None,
        },
        # This next one represents a plant in the "Accepted Bid" state and requires new keys: offer_price and start_time
        {
            "name": "T_FFES-4",
            "status_class": "status-accepted-bid",
            "badge_class": "text-bg-info",
            "status_text": "Accepted Bid",
            "icon": "bi-hourglass-split",
            "actual_gen": 0,
            "fpn": 0,
            "mel": 60,
            "balancing_direction": None,
            "offer_price": 115,
            "start_time": "19:00",
        },
    ]
    current_datetime = datetime.now(timezone.utc)
    context = {
        "plants": plants_data,
        "search_query": search_query,
        "fuel_filter": fuel_filter,
        "sort_filter": sort_filter,
        "last_refreshed": current_datetime,
    }
    return render(request, "plant_status_board.html", context)
