import requests
from django.conf import settings
from django.utils import timezone

from etl.models import Metric, Plant, TimeSeriesData
from utils import get_settlement_period


class BMRSDataService:
    """
    A service class to handle fetching and processing data from the Elexon BMRS API.
    """

    BASE_URL = "https://data.elexon.co.uk/bmrs/api/v1"
    API_KEY = settings.BMRS_API_KEY

    def _make_api_call(
        self, endpoint: str, params: dict, response_key: str | None = None
    ) -> list:
        """Generic helper method to call the API and return the 'data' list."""
        params["apiKey"] = self.API_KEY
        params["format"] = "json"

        response = requests.get(f"{self.BASE_URL}{endpoint}", params=params)
        response.raise_for_status()

        if response_key:
            return response.json().get(response_key, [])
        else:
            return response.json()

    def get_latest_plant_data(self):
        """
        Fetches the latest snapshot of MEL and FPN for all major generation units.
        """
        now = timezone.now()
        settlement_date = now.strftime("%Y-%m-%d")
        period = get_settlement_period(now)

        mel_data = self._make_api_call(
            endpoint="/balancing/physical/all",
            params={
                "dataset": "MELS",
                "settlementDate": settlement_date,
                "settlementPeriod": period,
            },
            response_key="data",
        )
        fpn_data = self._make_api_call(
            endpoint="/balancing/physical/all",
            params={
                "dataset": "PN",
                "settlementDate": settlement_date,
                "settlementPeriod": period,
            },
            response_key="data",
        )

        if not mel_data and not fpn_data:
            return f"No data returned for {settlement_date} SP{period}."

        self._process_and_store_plant_data(mel_data, fpn_data)

        return f"Successfully processed {len(mel_data) + len(fpn_data)} records for {settlement_date} SP{period}."

    def _process_and_store_plant_data(self, mel_data: list, fpn_data: list):
        """
        Parses the MEL and FPN data, merges them, and stores the time-series data.
        """
        mel_metric, _ = Metric.objects.get_or_create(
            code="MEL", defaults={"name": "Maximum Export Limit", "default_units": "MW"}
        )
        fpn_metric, _ = Metric.objects.get_or_create(
            code="FPN",
            defaults={"name": "Final Physical Notification", "default_units": "MW"},
        )

        # Use dictionaries for efficient lookup
        plant_data = {}
        for item in mel_data:
            if not item.get("bmUnit"):
                continue  # Probably an aggregated record
            plant_data.setdefault(item["bmUnit"], {})["mel_value"] = item["levelFrom"]
        for item in fpn_data:
            if not item.get("bmUnit"):
                continue  # Probably an aggregated record
            plant_data.setdefault(item["bmUnit"], {})["fpn_value"] = item["levelFrom"]

        records_to_create = []

        for bm_unit, values in plant_data.items():
            plant, _ = Plant.objects.get_or_create(
                eic_code=bm_unit, defaults={"name": bm_unit}
            )

            # Assuming both MEL and FPN are for the same timestamp
            now = timezone.now()
            timestamp = now.replace(
                minute=30 if now.minute >= 30 else 0, second=0, microsecond=0
            )

            records_to_create.append(
                TimeSeriesData(
                    time=timestamp,
                    metric=mel_metric,
                    plant=plant,
                    value=values.get("mel_value", 0),
                )
            )
            records_to_create.append(
                TimeSeriesData(
                    time=timestamp,
                    metric=fpn_metric,
                    plant=plant,
                    value=values.get("fpn_value", 0),
                )
            )

        TimeSeriesData.objects.bulk_create(records_to_create, ignore_conflicts=True)

    def get_latest_acceptances(self):
        """
        Fetches the latest 100 market-wide bid-offer acceptances (BOALF).
        """
        # This endpoint returns the latest 100 acceptances
        acceptance_data = self._make_api_call(
            endpoint="/balancing/acceptances/all/latest",
            params={},
            # The response is nested under a 'data' key
            response_key="data",
        )

        if not acceptance_data:
            return "No new acceptance data returned from API."

        self._process_and_store_acceptance_data(acceptance_data)

        return f"Successfully processed {len(acceptance_data)} acceptance records."

    def _process_and_store_acceptance_data(self, acceptance_data: list):
        """
        Parses Bid-Offer Acceptance data and stores it as time-series records.
        """
        level_from_metric, _ = Metric.objects.get_or_create(
            code="BOA-FROM",
            defaults={"name": "Bid-Offer Acceptance From Level", "default_units": "MW"},
        )
        level_to_metric, _ = Metric.objects.get_or_create(
            code="BOA-TO",
            defaults={"name": "Bid-Offer Acceptance To Level", "default_units": "MW"},
        )
        volume_metric, _ = Metric.objects.get_or_create(
            code="BOA-VOL",
            defaults={"name": "Bid-Offer Acceptance Volume", "default_units": "MW"},
        )

        records_to_create = []

        for item in acceptance_data:
            bm_unit_id = item.get("nationalGridBmUnit")
            if not bm_unit_id:
                continue

            plant, _ = Plant.objects.get_or_create(
                eic_code=bm_unit_id, defaults={"name": bm_unit_id}
            )

            timestamp_str = item.get("acceptanceTime")
            if not timestamp_str:
                continue

            # --- FIX: Remove the redundant timezone.make_aware() call ---
            # The fromisoformat method already produces a timezone-aware datetime
            # object because the string contains the UTC offset.
            timestamp = timezone.datetime.fromisoformat(
                timestamp_str.replace("Z", "+00:00")
            )
            # --- END FIX ---

            level_from = item.get("levelFrom", 0)
            level_to = item.get("levelTo", 0)
            volume = level_to - level_from

            records_to_create.append(
                TimeSeriesData(
                    time=timestamp,
                    metric=level_from_metric,
                    plant=plant,
                    value=level_from,
                )
            )
            records_to_create.append(
                TimeSeriesData(
                    time=timestamp, metric=level_to_metric, plant=plant, value=level_to
                )
            )
            records_to_create.append(
                TimeSeriesData(
                    time=timestamp, metric=volume_metric, plant=plant, value=volume
                )
            )

        TimeSeriesData.objects.bulk_create(records_to_create, ignore_conflicts=True)

    def update_plant_reference_data(self):
        """
        Fetches the master list of all BM Units and updates their fuel type
        and other descriptive data in our Plant model.
        """
        plant_list = self._make_api_call(endpoint="/reference/bmunits/all", params={})

        if not plant_list:
            return "No plant reference data returned from API."

        updated_count = 0
        created_count = 0
        for plant_info in plant_list:
            if not plant_info.get("elexonBmUnit"):
                continue

            # Use update_or_create to efficiently update our Plant database
            _, created = Plant.objects.update_or_create(
                eic_code=plant_info["elexonBmUnit"],
                defaults={
                    "name": plant_info.get("bmUnitName", "UNKNOWN") or "UNKNOWN",
                    "fuel_type": plant_info.get("fuelType", "UNKNOWN") or "UNKNOWN",
                    "generation_capacity": plant_info.get("generationCapacity"),
                    "bm_unit_type": plant_info.get("bmUnitType"),
                    "lead_party_name": plant_info.get("leadPartyName"),
                },
            )
            if created:
                created_count += 1
            else:
                updated_count += 1

        return f"Plant reference data updated. Updated: {updated_count}, Created: {created_count}."
