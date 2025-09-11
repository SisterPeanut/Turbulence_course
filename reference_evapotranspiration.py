"""
Compute hourly and daily reference evapotranspiration (ET0) from meteorological data
using the ASCE/FAO-56 Penman–Monteith hourly formulation.

Assumptions & mapping to your file:
- File: whitespace separated
- We use measurements at (approx) the heights given in the doc:
    * Air potential temperature at level 2 (Theta2 ~ 1.95 m) -> convert to actual T2m
    * Relative humidity at level 2 (r2, %) -> actual vapor pressure
    * Wind speed at level 4 (U4 ~ 10.1 m) -> convert to u2 (2 m)
    * Pressure column 'p' in hPa
    * Net radiation 'Rn' and ground heat flux 'G' in W/m^2 (10-min means)
- Time format: "hour.t" where fractional part is tenths of an hour interpreted as tens of minutes:
    e.g., 0.1 -> 00:10, 1.5 -> 01:50, 23.2 -> 23:20
- This script aggregates 10-min means to hourly means (recommended for hourly PM).
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# -----------------------------
# 1. Load the data
# -----------------------------
file_path = "FALL2_1.TXT"   

colnames = [
    "year", "month", "day", "time_decimal_h",
    "wind_speed", "potential_temperature", "relative_humidity",
    "air_pressure", "net_radiation", "ground_heat_flux"
]

df = pd.read_csv(file_path, delim_whitespace=True, header=None, names=colnames)

# Fix 2-digit years (94 -> 1994, etc.)
df['year'] = df['year'].apply(lambda y: int(1900 + y) if y > 50 else int(2000 + y))

# -----------------------------
# 2. Parse datetime
# -----------------------------
