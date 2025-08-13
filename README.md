# GridSight
The energy transition is a multi-decade megatrend that guarantees one thing: increasing market complexity and volatility. The value in this new market will accrue to those who can navigate this complexity most effectively. 

GridSight is a web-based intelligence tool for this new era, providing the speed of insight necessary to manage risk, identify opportunities, and trade with confidence.

## Project description

GridSight visualises public data and helps analyse historic and current scenarios in a way that can lead to forming better hypotheses and making more informed trading decisions.

It consists of two core, complementary views: a Live Plant Status Board that answers the tactical question, "What is happening to every major asset on the grid right now?" and a Historical Volatility Analyser which answers the strategic question, "What happened to prices and generation the last time conditions were exactly like this?"

## Core features

  1. Live Plant Status Board (the "Bingo Board"): A real-time, tile-based dashboard displaying the operational status of every major UK power generation unit. Each tile is colour-coded to show its status (e.g., Generating, Standby, Balancing, Outage) and provides key data at a glance: real-time output vs. planned (FPN) and maximum availability (MEL).

  2. Historical Volatility Analyser: An interactive dashboard which allows users to query years of historical grid data. Its primary feature is a Correlation Filter that isolates specific market conditions (e.g., low wind, high demand) and instantly displays the resulting average generation mix, imbalance prices, and thermal profitability.

  3. Indicative Spark Spread Calculator: An integrated feature that calculates and visualises the indicative profitability of gas-fired power plants, incorporating user-defined assumptions for thermal efficiency.

  4. System Headroom View: A macro-level chart that aggregates MEL and FPN data for the entire CCGT fleet, providing a clear, time-series view of the total spare capacity (headroom) available on the grid.


## Getting Started

This guide will walk you through setting up the GridSight project for local development.

### Prerequisites

* **Python 3.12**
* **PostgreSQL 16** (or later).
* The **TimescaleDB extension** must be installed and enabled on your PostgreSQL instance.

### Setup Instructions

1.  **Clone the repository:**
    ```bash
    git clone git@github.com:a115/gridsight.git
    cd gridsight
    ```

2.  **Create a virtual environment, activate it and install dependencies:**
    ```bash
    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    pip install -r requirements-dev.txt
    ```

3.  **Configure your environment:**
    Create a `.env` file in the project root by copying the example file. This will store your database credentials and other secrets / env vars.
    ```
    POSTGRES_PASSWORD=YOUR_PASSWORD
    DJANGO_SECRET_KEY=your-secret-key-here
    DJANGO_DEBUG=True
    ```

5.  **Run database migrations and collect static files:**
    This will create all the necessary tables in your database, including the TimescaleDB hypertables.
    ```bash
    python manage.py migrate
    python manage.py collectstatic
    ```

6.  **Run the development server:**
    ```bash
    python manage.py runserver
    ```
    The application should now be running at `http://127.0.0.1:8000/`.

7.  **Fetch initial data (Optional but Recommended):**
    To populate your local database with some sample data, you can use the custom management command.
    ```bash
    # TODO
    ```

