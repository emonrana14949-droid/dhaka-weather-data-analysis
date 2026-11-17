# Project Guide — Dhaka Weather Data Analysis

This guide explains **everything** in this project, step by step, in simple words. Read it from the top and you will understand the whole project — the data, the code, the charts and the results — even if you are a complete beginner.

---
## 1. What is this project?

This is a **Data Science project** about the weather of **Dhaka, Bangladesh**. It studies one full year of daily weather — **365 days of 2025** — and looks at temperature, feels-like temperature, humidity, rainfall, wind speed and air quality (AQI).

The project uses three Python tools: **NumPy** (to create the data and do number work), **Pandas** (to clean the data and make summary tables) and **Matplotlib** (to draw the charts).
### Questions this project answers

1. Which month is the hottest, and which is the coolest?
2. Which month has the most rain?
3. Which month has the worst air quality?
4. Are humidity and temperature related to each other?
5. What was the hottest single day? What was the rainiest single day?
6. How many rainy days are there in one year?
### Very important: the data is NOT real

The dataset is **synthetic data**. That means a computer **created** it with random numbers. Nobody measured this weather with real instruments.

But it is not random nonsense. It was **modelled on Dhaka's real seasons**: winter (Nov–Feb) is cool and dry and the air quality is poor; summer (Mar–May) is hot; the monsoon (Jun–Oct) brings heavy rain and high humidity. So the patterns look realistic, and they are perfect for **practising** the Data Science workflow: create data → clean it → analyse it → draw charts → write down what you found.

---
## 2. What is inside the project?

Here is every folder and file, one by one.

```text
dhaka-weather-data-analysis/
├── README.md
├── PROJECT_GUIDE.md          ← this file
├── requirements.txt
├── .gitignore
├── data/dhaka_weather_2025.csv
├── src/generate_dataset.py
├── src/analysis.py
├── notebooks/dhaka_weather_analysis.ipynb
└── outputs/
    ├── insights.md
    ├── tables/   (summary_statistics, monthly_weather_summary, season_summary, correlation_matrix)
    └── charts/   (daily_temperature_trend, monthly_rainfall, humidity_vs_temperature, air_quality_distribution)
```

- **README.md** — the short front page of the project: topic, questions, columns and quick-start commands.
- **PROJECT_GUIDE.md** — this guide: the full, slow explanation of everything.
- **requirements.txt** — a shopping list of Python libraries the project needs: `pandas`, `numpy`, `matplotlib`. One command installs them all.
- **.gitignore** — a small file that tells Git which junk files to ignore (like `__pycache__` folders). You never need to open it.
- **data/dhaka_weather_2025.csv** — the dataset itself. A CSV file is a simple table saved as text: rows are days, columns are measurements. This file has 365 rows (one per day) and 9 columns.
- **src/generate_dataset.py** — the first script. It **creates** the dataset with NumPy and saves it as the CSV file above. ("src" means "source code".)
- **src/analysis.py** — the second script. It **reads** the CSV with Pandas, cleans it, makes summary tables and charts, and writes the key findings.
- **notebooks/dhaka_weather_analysis.ipynb** — a Jupyter Notebook version for exploring the data interactively, cell by cell, if you want to play with it.
- **outputs/tables/** — the four summary tables the analysis saves as CSV files (explained in Section 7).
- **outputs/charts/** — the four chart images (PNG files) the analysis saves.
- **outputs/insights.md** — a short report file that the analysis writes by itself. It lists the key results in plain sentences.

---
## 3. The dataset, column by column

Every row is **one day**. Every column is **one measurement** of that day.

| Column | What it means | Example values |
|---|---|---|
| `date` | The day of the record, written as year-month-day | `2025-01-01`, `2025-06-16` |
| `month` | The month number, 1 to 12 | `1` (January), `7` (July) |
| `season` | The season of that month: Winter (Nov–Feb), Summer (Mar–May) or Monsoon (Jun–Oct) | `Winter`, `Summer`, `Monsoon` |
| `temperature_c` | The day's temperature in degrees Celsius (°C) | `23.13`, `36.68` |
| `feels_like_c` | How hot the day *feels* to a person. Humidity makes it feel hotter, so this is a bit higher than the real temperature | `25.85`, `22.31` |
| `humidity_percentage` | How much water vapour is in the air, in percent (%). High humidity feels sticky | `64.89`, `51.54` |
| `rainfall_mm` | How much rain fell that day, in millimetres (mm). `0` means a dry day | `0.0`, `80.00` |
| `wind_speed_kmh` | Wind speed in kilometres per hour (km/h) | `5.3`, `8.5` |
| `air_quality_index` | AQI — the Air Quality Index. It says how clean or dirty the air is. **Higher number = worse air** | `200.56`, `95.00` |

The first row of the real file is: `2025-01-01, 1, Winter, 23.13, 25.85, 64.89, 0.0, 5.3, 200.56`. Read it as: "On 1 January 2025 (winter), the temperature was 23.13 °C, it felt like 25.85 °C, humidity was 64.89%, there was no rain, the wind was 5.3 km/h, and the AQI was 200.56 — quite poor air, which is typical for Dhaka in winter."

---
## 4. How to run the project from zero

**Step 1 — Install Python.** Install Python 3 from [python.org](https://www.python.org/downloads/) if you do not have it. Check it works by opening a terminal and typing `python --version`.

**Step 2 — Go into the project folder:**

```bash
cd dhaka-weather-data-analysis
```

**Step 3 — Install the three libraries:**

```bash
pip install -r requirements.txt
```

This reads `requirements.txt` and installs Pandas, NumPy and Matplotlib.

**Step 4 — Create the dataset:**

```bash
python src/generate_dataset.py
```

You will see: `Dataset created: ... Rows: 365 | Columns: 9`. The file `data/dhaka_weather_2025.csv` is now created (or refreshed).

**Step 5 — Run the analysis:**

```bash
python src/analysis.py
```

This takes a few seconds. It prints `Analysis complete.` plus the hottest, wettest and worst-AQI months.

**Step 6 — See the outputs.** Read the results in `outputs/insights.md`; look at the pictures (PNG files) in `outputs/charts/`; look at the numbers (CSV files) in `outputs/tables/` — they open nicely in Excel, Google Sheets or any text editor.

**Order matters:** always run `generate_dataset.py` **before** `analysis.py`, because the analysis needs the CSV file to exist first.

---
## 5. Code explanation: `src/generate_dataset.py`

This script **creates the weather data**. It runs top to bottom. Let us walk through it in the same order.
### 5.1 Imports and file paths

```python
from pathlib import Path
import numpy as np
import pandas as pd
```

`import numpy as np` loads NumPy with the short name `np`; `import pandas as pd` loads Pandas as `pd`; `Path` helps the script find the project folder, so it saves the CSV in the right place no matter where you run it from.

```python
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / "data" / "dhaka_weather_2025.csv"
```

This simply says: "the dataset will be saved in the `data` folder, with the name `dhaka_weather_2025.csv`."
### 5.2 A helper: which season is this month?

```python
def season_for_month(month: int) -> str:
    if month in (11, 12, 1, 2):
        return "Winter"
    if month in (3, 4, 5):
        return "Summer"
    return "Monsoon"  # June to October
```

A small function that turns a month number into a season name, using the Bangladesh seasons defined for this project.
### 5.3 The random seed — why 42?

```python
rng = np.random.default_rng(42)
```

`rng` is the **random number generator**. The number `42` is the **seed**. Random numbers are different every time you run a program — unless you set a seed. With the same seed, the generator makes the **same** "random" numbers every run, so anyone who runs this script gets **exactly the same dataset** and the same results. That is very important for a project: your teacher can run your code and see the same numbers you reported. (Why 42? Any number works — 42 is a popular joke number in programming culture.)
### 5.4 The calendar

```python
dates = pd.date_range("2025-01-01", "2025-12-31", freq="D")
```

Pandas creates all 365 dates of 2025, one per day (`freq="D"` means daily). The script also takes the day-of-year (1–365) and the month (1–12) from these dates, and uses the helper function to label each day with its season.
### 5.5 Temperature — the sine curve

```python
temperature = (
    26
    + 5.5 * np.sin(2 * np.pi * (day_of_year - 40) / 365.25)
    + rng.normal(0, 1.8, size=n)
)
temperature = np.clip(temperature, 12, 40)
```

This is the cleverest part. Real temperature does not jump randomly — it rises and falls **smoothly** over the year: cool in January, hot around May, then a bit cooler in the monsoon and winter again. A **sine wave** (`np.sin`) is a smooth up-and-down curve — perfect for this:

- `26` is the middle level: the year is centred on about 26 °C.
- `5.5 * np.sin(...)` swings the temperature about 5.5 °C above and below that middle, over one full year (365.25 days). The `- 40` shift makes the peak of the curve land around **May**, Dhaka's hottest time.
- `rng.normal(0, 1.8, size=n)` adds small daily noise — real weather is never perfectly smooth, so each day wiggles by roughly ±1.8 °C.
- `np.clip(temperature, 12, 40)` cuts off impossible values: no day is colder than 12 °C or hotter than 40 °C.
### 5.6 Humidity — based on the season

```python
humidity_base = np.select(
    [season == "Winter", season == "Summer", season == "Monsoon"],
    [56, 66, 85],
)
humidity = np.clip(humidity_base + rng.normal(0, 6, size=n), 45, 98)
```

`np.select` picks a starting value by season: dry winter air starts at 56%, summer at 66%, and the wet monsoon at 85%. Then a little noise is added and the result is clipped to a realistic 45–98%.
### 5.7 Feels-like temperature

```python
humidity_factor = (humidity - 45) / (98 - 45)
feels_like = temperature + 1 + 4 * humidity_factor + rng.normal(0, 0.5, size=n)
```

Humid air feels hotter than dry air. So the feels-like temperature is the real temperature **plus 1 to 5 degrees**, and the "plus" is bigger when humidity is higher. `humidity_factor` is just humidity rescaled to a 0-to-1 number so it can control that bonus.
### 5.8 Rainfall — zero-inflated

```python
rainfall = np.zeros(n)   # start with no rain on any day
```

Rain is **zero-inflated**: most days have exactly **0 mm**, and only some days have rain. So the script starts with zeros for every day, then loops through the year and adds rain only on some days, by season:

- **Winter months** (Nov–Feb): only a 6% chance of rain on a day, and light.
- **Summer months** (Mar–May): a 25% chance — pre-monsoon showers and storms.
- **Monsoon core** (Jun–Sep): a 65% chance, and often heavy — most rainy days get between 5 and 80 mm.
- **October**: a 35% chance, as the monsoon retreats.

The amounts come from `rng.gamma(...)`, a random distribution that makes many small values and a few big ones — just like real rain. Finally everything is clipped to 0–80 mm.
### 5.9 Wind and air quality — also by season

Wind uses `np.where`: monsoon days start breezier (base 14 km/h) than other days (base 9 km/h), plus noise, clipped to 4–30 km/h.

AQI uses `np.select` again, with season bases: Winter **190** (poor — in the dry season dust and smoke stay trapped near the ground), Summer **130**, Monsoon **95** (cleanest — rain washes dust out of the air). Noise is added and the result is clipped to 60–280.
### 5.10 Saving the CSV

```python
df = pd.DataFrame({...})
df.to_csv(DATA_PATH, index=False)
```

All the columns are packed into a Pandas **DataFrame** (a table), the numbers are rounded to 2 decimals, and `to_csv` writes the table to `data/dhaka_weather_2025.csv`. `index=False` means "do not write the row numbers as an extra column."

---
## 6. Code explanation: `src/analysis.py`

This script **reads the dataset and produces everything in `outputs/`**. Again, we go in order.
### 6.1 Setup

The script imports Pandas, NumPy and Matplotlib, finds the project folders, and chooses a chart style:

```python
try:
    plt.style.use("seaborn-v0_8-whitegrid")
except OSError:
    plt.style.use("ggplot")
```

It tries a clean grid style for the charts; if that style is missing on your computer, it falls back to another style instead of crashing. `MONTH_NAMES` is a small dictionary that turns month numbers into names (1 → January, 2 → February, …) for the final report.
### 6.2 Loading the data — with date parsing

```python
df = pd.read_csv(DATA_PATH, parse_dates=["date"])
```

`pd.read_csv` loads the CSV into a DataFrame called `df`. `parse_dates=["date"]` is important: it tells Pandas "the `date` column is real **dates**, not text." Only then can Pandas sort by date, group by month, and draw a proper time line.
### 6.3 Cleaning

```python
df = df.drop_duplicates().copy()
df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors="coerce")
df = df.sort_values("date").reset_index(drop=True)
```

Three simple cleaning steps: (1) **drop duplicates** — remove any repeated day rows; (2) **make sure numbers are numbers** — `pd.to_numeric` converts the six measurement columns to numbers, and anything that cannot be converted becomes `NaN` (missing) instead of crashing the program; (3) **sort by date** — put the days in calendar order, then renumber the rows neatly from 0.
### 6.4 The summary tables

**Overall statistics** — one command describes every column:

```python
df.describe(include="all").round(2).to_csv(TABLE_DIR / "summary_statistics.csv")
```

`describe()` gives count, mean, standard deviation, minimum, quartiles and maximum for each column.

**Monthly summary** — the heart of the analysis:

```python
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
```

`groupby("month")` splits the 365 days into 12 groups, one per month. `.agg(...)` then calculates one row per month: the **average** temperature, the **total** rainfall (rain is added up, not averaged — a month's rain is the sum of its days), and the average humidity and AQI.

**Season summary** — the same idea with `groupby("season")`: days per season, average temperature, total rainfall, average humidity, wind and AQI for Winter, Summer and Monsoon.

**Correlation matrix**:

```python
corr = df[numeric_cols].corr(numeric_only=True).round(2)
```

`.corr()` compares every pair of number columns and gives a score from **−1 to +1**: near +1 means "when one goes up, the other goes up too", near −1 means "when one goes up, the other goes down", and near 0 means "no clear relationship". All four tables are saved as CSV files in `outputs/tables/`.
### 6.5 Chart 1 — daily temperature trend

```python
monthly_avg_temp = df.set_index("date").resample("M")["temperature_c"].mean()
```

`resample("M")` groups the daily data by **month** (a Pandas time-series tool) and takes the mean — the code uses `"M"` because the installed Pandas version accepts `"M"` for month-end groups. The chart then draws **two lines**: a thin, light line for every day's temperature, and a thick red line with dots for the monthly averages on top. The red line makes the yearly pattern easy to see through the daily wiggles. Saved as `daily_temperature_trend.png`.
### 6.6 Chart 2 — total rainfall by month

A **bar chart**: one bar per month, height = that month's total rainfall from the monthly table. The month labels are shortened (Jan, Feb, …). Saved as `monthly_rainfall.png`.
### 6.7 Chart 3 — humidity vs temperature scatter

```python
ax.scatter(df["humidity_percentage"], df["temperature_c"], ...)
slope, intercept = np.polyfit(df["humidity_percentage"], df["temperature_c"], 1)
```

Each dot is **one day**: its position shows that day's humidity (x-axis) and temperature (y-axis). `np.polyfit(..., 1)` asks NumPy to fit the best straight **trend line** through the dots, and the line is drawn in black. If the line clearly climbs or falls, the two things are related. Saved as `humidity_vs_temperature.png`.
### 6.8 Chart 4 — AQI distribution

A **histogram**: the AQI range is cut into 18 bins (bars), and each bar's height counts how many days fell in that range. A dashed black line marks the **mean** AQI. This shows what a "typical" day looks like and how often the air was really bad. Saved as `air_quality_distribution.png`. Every chart is saved with `fig.savefig(..., dpi=160)` (a sharp PNG image) and closed with `plt.close(fig)` to free memory.
### 6.9 Writing insights.md automatically

At the end, the script **finds the answers itself** from the tables:

```python
hottest_month_num = int(monthly["avg_temperature_c"].idxmax())
wettest_month_num = int(monthly["total_rainfall_mm"].idxmax())
worst_aqi_month_num = int(monthly["avg_air_quality_index"].idxmax())
```

`idxmax()` means "which month has the biggest value?" The script also finds the hottest single day, the rainiest single day, the total yearly rainfall and the number of rainy days, then writes them into a ready-made text template and saves it as `outputs/insights.md`. So the report is never typed by hand — it always matches the data.

---
## 7. How to read the outputs
### The charts

- **daily_temperature_trend.png** — Look at the red monthly-average line. It should climb from January to about May, stay high, then fall towards December. That smooth hill **is** the sine curve from the generator, coming back out of the data.
- **monthly_rainfall.png** — Compare the bar heights. The June–September bars should tower over the tiny winter bars. That is the monsoon.
- **humidity_vs_temperature.png** — Look at the black trend line. In this dataset it is almost flat, which matches the weak correlation of 0.11: knowing the humidity tells you very little about the temperature.
- **air_quality_distribution.png** — Look where the tall bars are. Many days sit at high AQI values (the winter pollution), with another group at lower values (the cleaner monsoon days). The dashed line is the average day.
### The tables

- **summary_statistics.csv** — The quick health check of the whole dataset: averages, spread (std), minimums and maximums for every column.
- **monthly_weather_summary.csv** — The main result table. Read it to find the hottest, wettest and most polluted months.
- **season_summary.csv** — The same story in three rows: Winter vs Summer vs Monsoon. The best table for a presentation slide.
- **correlation_matrix.csv** — A grid of numbers between −1 and +1. Look at pairs like temperature and feels-like: they move together strongly. Humidity and temperature barely move together (0.11). Remember: correlation shows a relationship, **not** a cause.

---
## 8. Key results of this project

These are the actual numbers from `outputs/insights.md` (synthetic data — learning results, not real weather records):

- Dataset size: **365 days** (1 January – 31 December 2025).
- Hottest month by average temperature: **May — 31.39 °C**.
- Wettest month by total rainfall: **July — 617.42 mm**.
- Worst air quality month by average AQI: **January — average AQI 194.98**.
- Correlation between humidity and temperature: **0.11** (very weak).
- Hottest single day: **20 May 2025 — 36.68 °C**.
- Rainiest single day: **16 June 2025 — 80.00 mm** of rain.
- Total rainfall for the year: **2,012.56 mm**, over **113 rainy days**.

In one sentence: *the year is hottest in May, the rain is concentrated in the monsoon (worst in July), the air is dirtiest in the dry winter (worst in January), and humidity and temperature are only weakly related.*

---
## 9. Viva / presentation help

Questions a teacher may ask — with short model answers you can say out loud.

**Q1. What is this project about?** It analyses one year of daily Dhaka weather — temperature, humidity, rain, wind and air quality — using Python. It finds monthly and seasonal patterns, like the hottest month, the wettest month and the worst air-quality month.

**Q2. Is this real weather data?** No. It is synthetic data created with NumPy, but it is modelled on Dhaka's real seasons — dry winter, hot summer, heavy monsoon. The goal is to practise the full Data Science workflow on realistic-looking data.

**Q3. Why did you use NumPy?** NumPy is fast for number work on whole arrays at once. I used it to generate the data (random numbers, the sine curve, clipping values) and to fit the trend line in the scatter chart with `polyfit`.

**Q4. Why Pandas? And what is a DataFrame?** A DataFrame is a table in Python — rows and columns, like a spreadsheet. Pandas makes it easy to load a CSV, clean it, group it by month or season, and calculate averages and totals with `groupby`.

**Q5. What is a time series?** Data recorded in time order — here, one row per day for 365 days. Because the order matters, we can use time tools like `parse_dates` and `resample("M")` to group days into months.

**Q6. Why does the temperature use a sine curve?** Real temperature changes smoothly over the year — it rises to a peak and falls again. A sine wave has exactly that smooth up-and-down shape, so it is a simple, realistic way to model the seasons. Daily noise is added so it does not look perfectly smooth.

**Q7. What does "zero-inflated" rainfall mean?** Most days have exactly zero rain, and only some days have any. So the generator starts with zeros and adds rain only on randomly chosen days, with the chance and the amount depending on the season — a 65% chance in the monsoon core, only 6% in winter.

**Q8. Why is the AQI worst in winter in this data?** The generator gives winter the highest base AQI (190), because in the dry season dust and smoke stay in the air. In the monsoon, rain washes the air cleaner, so the base is lowest (95). January came out worst, with an average AQI of 194.98.

**Q9. What is correlation? Your humidity–temperature correlation is 0.11 — what does that mean?** Correlation measures how two things move together, from −1 to +1. 0.11 is close to zero, so humidity and temperature have almost **no** linear relationship in this dataset. And correlation never proves that one thing *causes* the other.

**Q10. Why did you set the random seed to 42?** So the results are reproducible. With the same seed, anyone who runs the generator gets exactly the same dataset and the same results that I reported.

**Q11. What would you do differently with real data?** I would document the source, check for missing days, and handle them carefully instead of generating values. The analysis code would stay almost the same — only the CSV would change.

---
## 10. What to learn next / how to extend this project

1. **Use real data.** Replace the synthetic CSV with observed weather from the **Bangladesh Meteorological Department (BMD)** or an open weather API (for example Open-Meteo, which has free historical data). Keep the same columns, and the whole analysis runs unchanged.
2. **Compare two years.** Generate or download 2024 and 2025, put them in one table, and compare the monthly summaries side by side. Are the monsoons getting wetter?
3. **Add a simple prediction.** Use the sine curve idea to predict next month's average temperature, or try a basic machine-learning model with scikit-learn later.
4. **Make it interactive.** Turn the charts into a small **Streamlit** dashboard where a user can pick a month and see its weather summary.

---

*End of guide. If you can explain Sections 5 and 6 in your own words, you understand this project.*
