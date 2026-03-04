from django.contrib import admin

from etl.models import Metric, Plant, TimeSeriesData


@admin.register(Metric)
class MetricAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Metric model.
    """

    list_display = ("name", "code", "default_units")
    search_fields = ("name", "code")


@admin.register(Plant)
class PlantAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Plant model.
    """

    list_display = (
        "name",
        "eic_code",
        "fuel_type",
        "generation_capacity",
        "bm_unit_type",
        "lead_party_name",
    )
    search_fields = ("name", "eic_code", "lead_party_name")
    list_filter = ("fuel_type", "bm_unit_type")


@admin.register(TimeSeriesData)
class TimeSeriesDataAdmin(admin.ModelAdmin):
    """
    Admin configuration for the TimeSeriesData model.
    Optimized for handling large volumes of time-series data.
    """

    list_display = ("time", "metric", "plant", "value")

    list_filter = ("metric", "plant__fuel_type")

    date_hierarchy = "time"

    search_fields = ("metric__name", "plant__name", "plant__eic_code")

    # Make the data read-only in the admin to prevent accidental changes.
    # This data should be considered immutable once ingested.
    readonly_fields = ("time", "metric", "plant", "value")

    # To improve performance on this potentially huge table, we disable
    # the full count of all records, which can be slow.
    show_full_result_count = False

    # Set a reasonable number of items per page
    list_per_page = 100

    def has_add_permission(self, request):
        # Disable the ability to manually add time-series data via the admin
        return False

    def has_change_permission(self, request, obj=None):
        # Disable the ability to change time-series data via the admin
        return False
