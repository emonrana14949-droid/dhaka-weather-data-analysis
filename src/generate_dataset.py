"""Generate a synthetic daily weather dataset for Dhaka, 2025.

The dataset is practice data only. It is modelled on Dhaka's real seasonal
patterns (cool dry winter, hot summer, heavy monsoon rain, worse winter air
quality) so the Pandas, NumPy and visualization workflow can be practised on
realistic-looking weather data.
"""

from pathlib import Path

import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / "data" / "dhaka_weather_2025.csv"


def season_for_month(month: int) -> str:
    if month in (11, 12, 1, 2):
        return "Winter"
    if month in (3, 4, 5):
        return "Summer"
    return "Monsoon"  # June to October


def main() -> None:
    rng = np.random.default_rng(42)

    dates = pd.date_range("2025-01-01", "2025-12-31", freq="D")
    n = len(dates)
    day_of_year = dates.dayofyear.to_numpy()
    month = dates.month.to_numpy()
    season = np.array([season_for_month(m) for m in month])

    # Temperature: yearly sine curve peaking around May, plus daily noise.
    temperature = (
        26
        + 5.5 * np.sin(2 * np.pi * (day_of_year - 40) / 365.25)
        + rng.normal(0, 1.8, size=n)
    )
    temperature = np.clip(temperature, 12, 40)

    # Humidity: highest in the monsoon, lowest in winter.
    humidity_base = np.select(
        [season == "Winter", season == "Summer", season == "Monsoon"],
        [56, 66, 85],
    )
    humidity = np.clip(humidity_base + rng.normal(0, 6, size=n), 45, 98)

    # Feels-like temperature: 1-5 degrees above actual, more when humid.
    humidity_factor = (humidity - 45) / (98 - 45)
    feels_like = temperature + 1 + 4 * humidity_factor + rng.normal(0, 0.5, size=n)

    # Rainfall: zero-inflated. Dry winters; frequent heavy rain in the monsoon.
    rainfall = np.zeros(n)
    for i, m in enumerate(month):
        if m in (12, 1, 2, 11):  # winter: rare, light rain
            if rng.random() < 0.06:
                rainfall[i] = rng.gamma(shape=1.5, scale=2.0)
        elif m in (3, 4, 5):  # summer: occasional pre-monsoon showers / storms
            if rng.random() < 0.25:
                rainfall[i] = rng.gamma(shape=2.0, scale=6.0)
        elif m in (6, 7, 8, 9):  # monsoon core: frequent, often heavy
            if rng.random() < 0.65:
                rainfall[i] = np.clip(rng.gamma(shape=2.0, scale=14.0), 5, 80) if rng.random() < 0.7 else rng.gamma(shape=1.5, scale=3.0)
        else:  # October: monsoon retreating
            if rng.random() < 0.35:
                rainfall[i] = rng.gamma(shape=2.0, scale=8.0)
    rainfall = np.clip(rainfall, 0, 80)

    # Wind: breezier during the monsoon months.
    wind_base = np.where(season == "Monsoon", 14, 9)
    wind = np.clip(wind_base + rng.normal(0, 3.5, size=n), 4, 30)

    # Air quality: worst in the dry winter, cleanest in the rainy monsoon.
    aqi_base = np.select(
        [season == "Winter", season == "Summer", season == "Monsoon"],
        [190, 130, 95],
    )
    aqi = np.clip(aqi_base + rng.normal(0, 25, size=n), 60, 280)

    df = pd.DataFrame(
        {
            "date": dates.strftime("%Y-%m-%d"),
            "month": month,
            "season": season,
            "temperature_c": np.round(temperature, 2),
            "feels_like_c": np.round(feels_like, 2),
            "humidity_percentage": np.round(humidity, 2),
            "rainfall_mm": np.round(rainfall, 2),
            "wind_speed_kmh": np.round(wind, 2),
            "air_quality_index": np.round(aqi, 2),
        }
    )

    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(DATA_PATH, index=False)
    print(f"Dataset created: {DATA_PATH}")
    print(f"Rows: {len(df)} | Columns: {len(df.columns)}")


if __name__ == "__main__":
    main()
