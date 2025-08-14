Data Sources
=============

## Elexon BMRS API

| Data Point           | Primary Source              | API Endpoint            | Params       | Notes                                                              |
|----------------------|-----------------------------|-------------------------|--------------|--------------------------------------------------------------------|
| Generation by Fuel   | Elexon BMRS API             | `B1610` ?               |              | Core data for wind, gas (CCGT), nuclear, etc. generation in MW.    |
| Imbalance Price      | Elexon BMRS API             | `B1770` ?               |              | System Buy Price in £/MWh.                                         |
| System Demand        | Elexon BMRS API             | `B0620` ?               |              | Day-Ahead Total Load Forecast used for filtering.                  |
| FPN (Planned Gen)    | Elexon Insights API         | /balancing/physical/all | dataset=PN   | The Final Physical Notification for each BM Unit.                  |
| MEL (Max Gen)        | Elexon Insights API         | /balancing/physical/all | dataset=MELS | The Maximum Export Limit for each BM Unit.                         |
| BOALF                | Elexon Insights API         | /datasets/BOALF         |              | Bid-Offer Acceptances, showing forward-looking balancing actions.  |
| Plant Reference      | Elexon Insights API         | /reference/bmunits/all  |              | Master list of all BM Units with fuel type, capacity, etc.         |
| NBP Gas Price        | National Gas Data Portal    | `SAP`                   |              | Unit is p/therm; requires conversion. Used for spark spread.       |
| UKA Carbon Price     | Public Data Source (Ember?) | TBD (CSV download ?)    |              | Unit is £/tonne. Used for spark spread.                            |
