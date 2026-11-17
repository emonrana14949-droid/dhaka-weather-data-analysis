"""Analyse the Dhaka weather dataset with Pandas, NumPy and Matplotlib.

Run from the project root:
    python src/analysis.py

Outputs are saved to:
    outputs/tables/  (CSV summary tables)
    outputs/charts/  (PNG visualizations)
    outputs/insights.md
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / "data" / "dhaka_weather_2025.csv"
TABLE_DIR = PROJECT_ROOT / "outputs" / "tables"
CHART_DIR = PROJECT_ROOT / "outputs" / "charts"
INSIGHTS_PATH = PROJECT_ROOT / "outputs" / "insights.md"

MONTH_NAMES = {
    1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June",
    7: "July", 8: "August", 9: "September", 10: "October", 11: "November",
    12: "December",
}

try:
    plt.style.use("seaborn-v0_8-whitegrid")
except OSError:
    plt.style.use("ggplot")


def main() -> None:
    TABLE_DIR.mkdir(parents=True, exist_ok=True)
    CHART_DIR.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(DATA_PATH, parse_dates=["date"])

    # Basic cleaning.
    df = df.drop_duplicates().copy()
    numeric_cols = [
        "temperature_c", "feels_like_c", "humidity_percentage",
        "rainfall_mm", "wind_speed_kmh", "air_quality_index",
    ]
    df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors="coerce")
    df = df.sort_values("date").reset_index(drop=True)

    # Summary tables.
    df.describe(include="all").round(2).to_csv(TABLE_DIR / "summary_statistics.csv")

    monthly = (
        df.groupby("month")
        .agg(
            avg_temperature_c=("temperature_c", "mean"),
            total_rainfall_mm=("rainfall_mm", "sum"),
            avg_humidity_percentage=("humidity_percentage", "mean"),
            avg_air_quality_index=("air_quality_index", "mean"),
        )
        .round(2)
    )
    monthly.to_csv(TABLE_DIR / "monthly_weather_summary.csv")

    season_summary = (
        df.groupby("season")
        .agg(
            days=("date", "count"),
            avg_temperature_c=("temperature_c", "mean"),
            total_rainfall_mm=("rainfall_mm", "sum"),
            avg_humidity_percentage=("humidity_percentage", "mean"),
            avg_wind_speed_kmh=("wind_speed_kmh", "mean"),
            avg_air_quality_index=("air_quality_index", "mean"),
        )
        .round(2)
    )
    season_summary.to_csv(TABLE_DIR / "season_summary.csv")

    corr = df[numeric_cols].corr(numeric_only=True).round(2)
    corr.to_csv(TABLE_DIR / "correlation_matrix.csv")

    # Chart 1: daily temperature trend with monthly-average overlay.
    monthly_avg_temp = df.set_index("date").resample("M")["temperature_c"].mean()
    fig, ax = plt.subplots(figsize=(11, 5))
    ax.plot(df["date"], df["temperature_c"], color="#2f81f7", alpha=0.45, linewidth=0.8, label="Daily temperature")
    ax.plot(monthly_avg_temp.index, monthly_avg_temp.values, color="#d1242f", linewidth=2.2, marker="o", markersize=4, label="Monthly average")
    ax.set_title("Dhaka Daily Temperature Trend — 2025", fontweight="bold")
    ax.set_xlabel("Date")
    ax.set_ylabel("Temperature (°C)")
    ax.legend()
    fig.tight_layout()
    fig.savefig(CHART_DIR / "daily_temperature_trend.png", dpi=160)
    plt.close(fig)

    # Chart 2: total rainfall by month.
    fig, ax = plt.subplots(figsize=(10, 4.8))
    ax.bar(monthly.index, monthly["total_rainfall_mm"], color="#0969da", edgecolor="white")
    ax.set_xticks(monthly.index, [MONTH_NAMES[m][:3] for m in monthly.index])
    ax.set_title("Total Rainfall by Month — Dhaka 2025", fontweight="bold")
    ax.set_xlabel("Month")
    ax.set_ylabel("Total rainfall (mm)")
    fig.tight_layout()
    fig.savefig(CHART_DIR / "monthly_rainfall.png", dpi=160)
    plt.close(fig)

    # Chart 3: humidity vs temperature scatter with a NumPy trend line.
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.scatter(df["humidity_percentage"], df["temperature_c"], color="#8250df", alpha=0.55, edgecolor="white", linewidth=0.4)
    slope, intercept = np.polyfit(df["humidity_percentage"], df["temperature_c"], 1)
    x_line = np.linspace(df["humidity_percentage"].min(), df["humidity_percentage"].max(), 100)
    ax.plot(x_line, slope * x_line + intercept, color="#111111", linewidth=1.6, label="Trend line")
    ax.set_title("Humidity vs Temperature", fontweight="bold")
    ax.set_xlabel("Humidity (%)")
    ax.set_ylabel("Temperature (°C)")
    ax.legend()
    fig.tight_layout()
    fig.savefig(CHART_DIR / "humidity_vs_temperature.png", dpi=160)
    plt.close(fig)

    # Chart 4: air quality index distribution.
    fig, ax = plt.subplots(figsize=(9, 4.8))
    ax.hist(df["air_quality_index"], bins=18, color="#bf8700", edgecolor="white")
    ax.axvline(df["air_quality_index"].mean(), color="#111111", linestyle="--", linewidth=1.5, label="Mean")
    ax.set_title("Distribution of Air Quality Index (AQI)", fontweight="bold")
    ax.set_xlabel("Air Quality Index")
    ax.set_ylabel("Number of days")
    ax.legend()
    fig.tight_layout()
    fig.savefig(CHART_DIR / "air_quality_distribution.png", dpi=160)
    plt.close(fig)

    # Key findings for the insights file.
    hottest_month_num = int(monthly["avg_temperature_c"].idxmax())
    wettest_month_num = int(monthly["total_rainfall_mm"].idxmax())
    worst_aqi_month_num = int(monthly["avg_air_quality_index"].idxmax())
    temp_humidity_corr = corr.loc["humidity_percentage", "temperature_c"]
    hottest_day = df.loc[df["temperature_c"].idxmax()]
    rainiest_day = df.loc[df["rainfall_mm"].idxmax()]

    insights = f"""# Key Insights — Dhaka Weather Data Analysis

> This project uses synthetic practice data generated with NumPy, modelled on Dhaka's seasonal patterns. The findings below are for learning the workflow only; they are not real weather records.

- Dataset size: **{len(df)} days** (1 January – 31 December 2025).
- Hottest month by average temperature: **{MONTH_NAMES[hottest_month_num]}** ({monthly.loc[hottest_month_num, 'avg_temperature_c']:.2f} °C).
- Wettest month by total rainfall: **{MONTH_NAMES[wettest_month_num]}** ({monthly.loc[wettest_month_num, 'total_rainfall_mm']:.2f} mm).
- Worst air quality month by average AQI: **{MONTH_NAMES[worst_aqi_month_num]}** (average AQI {monthly.loc[worst_aqi_month_num, 'avg_air_quality_index']:.2f}).
- Correlation between humidity and temperature: **{temp_humidity_corr:.2f}**.
- Hottest single day: **{hottest_day['date'].date()}** at {hottest_day['temperature_c']:.2f} °C.
- Rainiest single day: **{rainiest_day['date'].date()}** with {rainiest_day['rainfall_mm']:.2f} mm of rain.
- Total rainfall for the year: **{df['rainfall_mm'].sum():.2f} mm**; rainy days (rainfall > 0): **{int((df['rainfall_mm'] > 0).sum())}**.

## Charts

- `charts/daily_temperature_trend.png`
- `charts/monthly_rainfall.png`
- `charts/humidity_vs_temperature.png`
- `charts/air_quality_distribution.png`

## Important note

This is synthetic data. For a real project, replace the CSV with observed data (for example from the Bangladesh Meteorological Department) and document the source and any missing days.
"""
    INSIGHTS_PATH.write_text(insights, encoding="utf-8")

    print("Analysis complete.")
    print(f"Tables saved to: {TABLE_DIR}")
    print(f"Charts saved to: {CHART_DIR}")
    print(f"Insights saved to: {INSIGHTS_PATH}")
    print(f"Hottest month: {MONTH_NAMES[hottest_month_num]} | Wettest month: {MONTH_NAMES[wettest_month_num]} | Worst AQI month: {MONTH_NAMES[worst_aqi_month_num]}")


if __name__ == "__main__":
    main()
