from django.shortcuts import render


def index(request):
    """
    View to render the main index/hub page.
    """
    context = {}
    return render(request, "index.html", context)


def historical_analyser_view(request):
    """
    View to render the historical analyser page.
    """
    # In the future, this view will query the database and pass data to the template.
    # For now, we use some mock data from our prototype.
    mock_labels = [
        "01:00",
        "02:00",
        "03:00",
        "04:00",
        "05:00",
        "06:00",
        "07:00",
        "08:00",
        "09:00",
        "10:00",
        "11:00",
        "12:00",
    ]

    chart_data = {
        "generation": {
            "labels": mock_labels,
            "datasets": [
                {
                    "label": "Wind Generation (MW)",
                    "data": [
                        12000,
                        11500,
                        11000,
                        9000,
                        7000,
                        5000,
                        4500,
                        4000,
                        3500,
                        3000,
                        2800,
                        2500,
                    ],
                    "borderColor": "rgb(25, 135, 84)",
                    "backgroundColor": "rgba(25, 135, 84, 0.1)",
                    "fill": True,
                    "tension": 0.3,
                },
                {
                    "label": "Gas (CCGT) Generation (MW)",
                    "data": [
                        8000,
                        8200,
                        8500,
                        10000,
                        12000,
                        15000,
                        16000,
                        18000,
                        19000,
                        20000,
                        21000,
                        21500,
                    ],
                    "borderColor": "rgb(255, 193, 7)",
                    "backgroundColor": "rgba(255, 193, 7, 0.1)",
                    "fill": True,
                    "tension": 0.3,
                },
            ],
        },
        "price": {
            "labels": mock_labels,
            "datasets": [
                {
                    "label": "Imbalance Price",
                    "data": [35, 38, 40, 45, 55, 65, 75, 95, 110, 105, 100, 98],
                    "borderColor": "rgb(220, 53, 69)",
                    "backgroundColor": "rgba(220, 53, 69, 0.1)",
                    "stepped": True,
                    "fill": True,
                }
            ],
        },
        "spread": {
            "labels": mock_labels,
            "datasets": [
                {
                    "label": "Indicative Spark Spread",
                    "data": [-5, -4, -2, 3, 8, 15, 20, 35, 48, 45, 42, 40],
                    # Dynamic coloring will be handled in JS
                    "backgroundColor": ["rgba(220, 53, 69, 0.6)"] * 3
                    + ["rgba(25, 135, 84, 0.6)"] * 9,
                    "borderColor": ["rgb(220, 53, 69)"] * 3 + ["rgb(25, 135, 84)"] * 9,
                    "borderWidth": 1,
                }
            ],
        },
        "mix": {
            "labels": ["Gas (CCGT)", "Wind", "Nuclear", "Imports", "Other"],
            "datasets": [
                {
                    "label": "Generation Mix",
                    "data": [45, 25, 15, 10, 5],
                    "backgroundColor": [
                        "rgb(255, 193, 7)",
                        "rgb(25, 135, 84)",
                        "rgb(13, 110, 253)",
                        "rgb(108, 117, 125)",
                        "rgb(200, 200, 200)",
                    ],
                    "hoverOffset": 4,
                }
            ],
        },
    }

    context = {
        "chart_data": chart_data,
    }
    return render(request, "historical_analyser.html", context)


def system_headroom_view(request):
    """
    View to render the System Headroom page.
    """

    # In the future, this view will query the database and pass data to the template.
    # For now, we use some mock data from our prototype.

    mock_labels = [
        "15:00",
        "15:30",
        "16:00",
        "16:30",
        "17:00",
        "17:30",
        "18:00",
        "18:30",
        "19:00",
        "19:30",
        "20:00",
    ]

    chart_data = {
        "labels": mock_labels,
        "datasets": [
            {
                "label": "Max Export Limit (MEL)",
                "data": [
                    22000,
                    22000,
                    21500,
                    21000,
                    21000,
                    21000,
                    21500,
                    22000,
                    22000,
                    22000,
                    22000,
                ],
                "borderColor": "rgba(13, 110, 253, 0.6)",
                "pointRadius": 0,
                "borderWidth": 2,
                "borderDash": [5, 5],
                "fill": False,
                "order": 1,
            },
            {
                "label": "Actual Generation (MW)",
                "data": [
                    16050,
                    16520,
                    17000,
                    17810,
                    19050,
                    20100,
                    20600,
                    21200,
                    21500,
                    20800,
                    19600,
                ],
                "borderColor": "rgb(25, 135, 84)",
                "backgroundColor": "rgba(25, 135, 84, 0.25)",
                "pointRadius": 2,
                "borderWidth": 2.5,
                "fill": {"target": "2"},
                "tension": 0.3,
                "order": 3,
            },
            {
                "label": "Planned Generation (FPN)",
                "data": [
                    16000,
                    16500,
                    17000,
                    17800,
                    19000,
                    20000,
                    20500,
                    21150,
                    21000,
                    20500,
                    19500,
                ],
                "borderColor": "rgb(108, 117, 125)",
                "backgroundColor": "rgba(13, 110, 253, 0.15)",
                "pointRadius": 0,
                "borderWidth": 1.5,
                "fill": {"target": "0"},
                "tension": 0.3,
                "order": 2,
            },
        ],
    }
    context = {"chart_data": chart_data}
    return render(request, "system_headroom.html", context)


def plant_status_board_view(request):
    """
    View to render the Live Plant Status Board.
    """

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
    context = {"plants": plants_data}
    return render(request, "plant_status_board.html", context)
