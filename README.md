# gridsight
A web-based intelligence tool for UK power traders. Visualises real-time grid status and automates historical volatility analysis to generate actionable insights.

## Project description

The UK power market is defined by extreme volatility, driven by the interplay between intermittent renewables and thermal generation. 

GridSight visualises public data and helps analyse historic and current scenarios in a way that can lead to forming better hypotheses and making more informed trading decisions.

It consists of two core, complementary views: a Live Plant Status Board that answers the tactical question, "What is happening to every major asset on the grid right now?" and a Historical Volatility Analyser which answers the strategic question, "What happened to prices and generation the last time conditions were exactly like this?"

## Core features

  1. Live Plant Status Board (the "Bingo Board"): A real-time, tile-based dashboard displaying the operational status of every major UK power generation unit. Each tile is colour-coded to show its status (e.g., Generating, Standby, Balancing, Outage) and provides key data at a glance: real-time output vs. planned (FPN) and maximum availability (MEL).

  2. Historical Volatility Analyser: An interactive dashboard which allows users to query years of historical grid data. Its primary feature is a Correlation Filter that isolates specific market conditions (e.g., low wind, high demand) and instantly displays the resulting average generation mix, imbalance prices, and thermal profitability.

  3. Indicative Spark Spread Calculator: An integrated feature that calculates and visualises the indicative profitability of gas-fired power plants, incorporating user-defined assumptions for thermal efficiency.

  4. System Headroom View: A macro-level chart that aggregates MEL and FPN data for the entire CCGT fleet, providing a clear, time-series view of the total spare capacity (headroom) available on the grid.


