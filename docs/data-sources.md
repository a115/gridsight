Data Sources
=============

## Elexon BMRS API

| Data Point           | Primary Source               | API Endpoint / Report Code | Granularity | Notes                                                              |
|----------------------|------------------------------|----------------------------|-------------|--------------------------------------------------------------------|
| Generation by Fuel   | Elexon BMRS API              | `B1610`                    | 30-min (HH) | Core data for wind, gas (CCGT), nuclear, etc. generation in MW.    |
| Imbalance Price      | Elexon BMRS API              | `B1770`                    | 30-min (HH) | System Buy Price in £/MWh.                                         |
| System Demand        | Elexon BMRS API              | `B0620`                    | 30-min (HH) | Day-Ahead Total Load Forecast used for filtering.                  |
| FPN (Planned Gen)    | Elexon BMRS API              | `B1440`                    | 30-min (HH) | Required for the "System Headroom" view.                           |
| MEL (Max Gen)        | Elexon BMRS API              | `B1720` / `ROUC`           | 30-min (HH) | For the "System Headroom" view. Research needed for best report.   |
| NBP Gas Price        | National Gas Data Portal API | `SAP`                      | Daily       | Unit is p/therm; requires conversion. Used for spark spread.       |
| UKA Carbon Price     | Public Data Source (Ember?)  | TBD (e.g., CSV download)   | Daily       | Unit is £/tonne. Used for spark spread.                            |
