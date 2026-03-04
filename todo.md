TODO
=====

Product:

1. Plug in some data into the mock **Volatility Analyser** dashboard
2. Plug in some data into the mock **System Headroom** dashboard
3. Plug in some data into the mock **Live Plant Status board** dashboard

Shared app setup/infra:
- Add healthcheck Celery task


first bingo baord /live plant - 
middle headroom - 
spark spread (volatility analyser) is what we call the first - Jordan


We can have different approaches

Celery tasks to begin with
Only as much testing as needed
ELEXON API is a free API, we just need a key and there is still limit rates


The view (viz/views_plant_status.py) and template (templates/plant_status_board.html)
for the "bingo board" are built but use a hardcoded list of Python dictionaries for data.

The BMRSDataService in etl/services.py already fetches and stores the MEL (Maximum Export Limit)
and FPN (Final Physical Notification) data into the TimeSeriesData model. You can start by querying
this model to populate the main generation figures for each plant.

The current ETL does not yet fetch balancing mechanism data (for "Balancing" status) or Bid-Offer Acceptances (for "Accepted Bid" status). The next step after integrating existing data will be to expand the BMRSDataService to fetch from the BOALF dataset mentioned in docs/data-sources.md


    # plants_data = [
    #     PlantStatusCard(
    #         name="T_DRAX-1",
    #         status_class=StatusClass.GENERATING,
    #         badge_class=BadgeClass.PRIMARY,
    #         status_text=StatusText.GENERATING,
    #         icon=None,
    #         actual_gen=640,
    #         fpn=640,
    #         mel=645,
    #         balancing_direction=None,
    #     ),
    #     PlantStatusCard(
    #         name="T_PEMB-21",
    #         status_class=StatusClass.BALANCING,
    #         badge_class=BadgeClass.WARNING,
    #         status_text=StatusText.BALANCING,
    #         icon=None,
    #         actual_gen=450,
    #         fpn=400,
    #         mel=510,
    #         balancing_direction=BalancingDirection.UP,
    #     ),
    #     PlantStatusCard(
    #         name="T_STAY-1",
    #         status_class=StatusClass.STANDBY,
    #         badge_class=BadgeClass.SUCCESS,
    #         status_text=StatusText.STANDBY,
    #         icon=None,
    #         actual_gen=0,
    #         fpn=0,
    #         mel=350,
    #         balancing_direction=None,
    #     ),
    #     PlantStatusCard(
    #         name="T_WBURB-1",
    #         status_class=StatusClass.TRIP,
    #         badge_class=BadgeClass.DANGER,
    #         status_text=StatusText.TRIP,
    #         icon="bi-exclamation-triangle-fill",
    #         actual_gen=0,
    #         fpn=450,
    #         mel=0,
    #         balancing_direction=None,
    #     ),
    #     PlantStatusCard(
    #         name="T_EGGPS-1",
    #         status_class=StatusClass.OUTAGE,
    #         badge_class=BadgeClass.SECONDARY,
    #         status_text=StatusText.OUTAGE,
    #         icon=None,
    #         actual_gen=0,
    #         fpn=0,
    #         mel=0,
    #         balancing_direction=None,
    #     ),
    #     PlantStatusCard(
    #         name="T_GRAIN-1",
    #         status_class=StatusClass.GENERATING,
    #         badge_class=BadgeClass.PRIMARY,
    #         status_text=StatusText.GENERATING,
    #         icon=None,
    #         actual_gen=420,
    #         fpn=420,
    #         mel=420,
    #         balancing_direction=None,
    #     ),
    #     PlantStatusCard(
    #         name="T_CORBY-1",
    #         status_class=StatusClass.STANDBY,
    #         badge_class=BadgeClass.SUCCESS,
    #         status_text=StatusText.STANDBY,
    #         icon=None,
    #         actual_gen=0,
    #         fpn=0,
    #         mel=180,
    #         balancing_direction=None,
    #     ),
    #     PlantStatusCard(
    #         name="T_HARTL-1",
    #         status_class=StatusClass.GENERATING,
    #         badge_class=BadgeClass.PRIMARY,
    #         status_text=StatusText.GENERATING,
    #         icon=None,
    #         actual_gen=595,
    #         fpn=595,
    #         mel=595,
    #         balancing_direction=None,
    #     ),
    #     # This next one represents a plant in the "Accepted Bid" state and requires new keys: offer_price and start_time
    #     PlantStatusCard(
    #         name="T_FFES-4",
    #         status_class=StatusClass.ACCEPTED_BID,
    #         badge_class=BadgeClass.INFO,
    #         status_text=StatusText.ACCEPTED_BID,
    #         icon="bi-hourglass-split",
    #         actual_gen=0,
    #         fpn=0,
    #         mel=60,
    #         balancing_direction=None,
    #         offer_price=115,
    #         start_time="19:00",
    #     ),
    # ]