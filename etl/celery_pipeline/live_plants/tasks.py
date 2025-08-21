from etl.celery_pipeline.celery import etl_app as app
import logfire


@app.task(bind=True, ignore_result=True)
def ingest_plants_data(self):
    # TODO: Implement the logic to ingest plants data
    logfire.info("Ingesting plants data")
