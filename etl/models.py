from django.db import models
from timescale.db.models.fields import TimescaleDateTimeField
from timescale.db.models.managers import TimescaleManager
from timescale.db.models.models import TimescaleModel


class Metric(models.Model):
    """Stores the definition of a metric, including its unit of measure."""

    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(
        max_length=50, unique=True, help_text="Internal code, e.g., B1610_WIND"
    )
    default_units = models.CharField(max_length=20, help_text="e.g., MW, £/MWh, p/th")

    def __str__(self):
        return f"{self.name} ({self.default_units})"


class Plant(models.Model):
    """Stores information about a specific power generation plant/unit."""

    name = models.CharField(max_length=100)
    eic_code = models.CharField(
        max_length=50, unique=True, help_text="Unique EIC code for the plant/unit"
    )
    fuel_type = models.CharField(max_length=50)
    generation_capacity = models.FloatField(null=True, blank=True)
    bm_unit_type = models.CharField(max_length=10, null=True, blank=True)
    lead_party_name = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name


class TimeSeriesData(TimescaleModel):
    """
    A TimescaleDB hypertable for storing all time-series data points.
    """

    time = TimescaleDateTimeField(interval="7 days")

    value = models.FloatField()
    metric = models.ForeignKey(
        Metric, on_delete=models.CASCADE, related_name="data_points"
    )

    # Optional foreign key to a specific plant for generation data.
    plant = models.ForeignKey(
        Plant,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="data_points",
    )

    # Add the TimescaleManager for time-series specific queries.
    # The standard 'objects' manager is still available.
    objects = models.Manager()
    timescale = TimescaleManager()

    class Meta:
        unique_together = ("time", "metric", "plant")
        ordering = ["-time", "metric"]

    def __str__(self):
        plant_name = f" ({self.plant.name})" if self.plant else ""
        return f"{self.metric.name}{plant_name} at {self.time}: {self.value} {self.metric.default_units}"

class BidOfferAcceptance(models.Model):
    """
    Stores data for a specific Bid-Offer Acceptance from the BOALF report.
    This is not a time-series model, but a record of a specific event.
    """
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE, related_name='acceptances')
    acceptance_number = models.IntegerField(unique=True)
    acceptance_time = models.DateTimeField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    volume = models.FloatField(help_text="The accepted volume in MW")
    # In the real API, there is no price field in the BOALF dataset.
    # This would need to be cross-referenced from the Bid-Offer endpoint if required.
    price = models.FloatField(null=True, blank=True, help_text="The accepted price in £/MWh")

    class Meta:
        ordering = ['-start_time']

    def __str__(self):
        return f"Acceptance {self.acceptance_number} for {self.plant.name} at {self.start_time}"