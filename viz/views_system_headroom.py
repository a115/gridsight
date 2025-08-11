from django.shortcuts import render


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
