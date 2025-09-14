from django.core.management.base import BaseCommand

from etl.services import BMRSDataService


class Command(BaseCommand):
    help = "Manually fetches data from the BMRS API."

    def add_arguments(self, parser):
        parser.add_argument(
            "source",
            type=str,
            help='Specify the data source to fetch: "latest_snapshot" or "plant_reference"',
        )

    def handle(self, *args, **options):
        source = options["source"]
        service = BMRSDataService()

        if source == "latest_snapshot":
            self.stdout.write("Starting manual fetch of latest plant data (MEL/FPN)...")
            result = service.get_latest_plant_data()
        elif source == "plant_reference":
            self.stdout.write(
                "Starting manual fetch of plant reference data (fuel types, etc.)..."
            )
            result = service.update_plant_reference_data()
        elif source == "latest_acceptances":
            self.stdout.write(
                "Starting manual fetch of latest 100 BOALF acceptances..."
            )
            result = service.get_latest_acceptances()
        else:
            self.stdout.write(
                self.style.ERROR(
                    f'Unknown source: {source}. Use "latest_snapshot" or "plant_reference".'
                )
            )
            return

        if result:
            self.stdout.write(self.style.SUCCESS(f"Fetch complete. {result}"))
        else:
            self.stdout.write(
                self.style.ERROR("Data fetch failed. Check logs for details.")
            )
