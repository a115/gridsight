Business requirements
======================

The Indicative Spark Spread calculation will be performed on the backend for each 30-minute settlement period using a formula like this:

```
Spark Spread (£/MWh) = Power Price (£/MWh) - (Gas Price [converted] / Thermal Efficiency) - (Carbon Price * Carbon Intensity)
```

- Power Price: Direct from B1770.
- Gas Price Conversion: The daily SAP (in p/therm) will be converted to £/MWh using a standard industry conversion factor.
- User-Defined Assumptions:
    - Thermal Efficiency: Default to 50%. The UI will allow the user to override this value.
    - Carbon Intensity of Gas: Use a fixed industry standard, e.g., 0.20 tCO2/MWh.

All electricity data will be processed at its native 30-minute settlement period granularity (though we should aim to support 15-minute periods).
Daily gas and carbon prices will be applied uniformly to all settlement periods within that gas day.
