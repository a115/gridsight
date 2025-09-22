from datetime import datetime, timezone

from django.shortcuts import render

from etl.models import Plant
from viz.plant_status.presentation import (
    PlantStatusCardResolver,
    PlantStatusViewContext,
)


def plant_status_board_view(request):
    """
    View to render the Live Plant Status Board.
    """

    search_query = request.GET.get("search", "")
    fuel_filter = request.GET.get("fuel_type", "all")
    sort_filter = request.GET.get("sort", "mel")

    # TODO: Implement filters
    plants_data = Plant.objects.all()[:10]

    plants_cards = [PlantStatusCardResolver.resolve(plant) for plant in plants_data]

    current_datetime = datetime.now(timezone.utc)
    context = PlantStatusViewContext(
        plants=plants_cards,
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
