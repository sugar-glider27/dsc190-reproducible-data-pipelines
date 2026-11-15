from pathlib import Path
import pandas as pd

INPUT = Path("data/transformed/events.csv")
OUTPUT = Path("data/features/events.csv")

df = pd.read_csv(
    INPUT,
    dtype={
        "user_id": "string",
        "timestamp": "string",
        "event_type": "string",
        "date": "string",
    },
)

df["duration_seconds"] = pd.to_numeric(
    df["duration_seconds"], errors="raise"
).astype("int64")

df["duration_minutes"] = df["duration_seconds"] / 60

dates = pd.to_datetime(df["date"], format="%Y-%m-%d", errors="raise")
weekday_names = ["Monday", "Tuesday", "Wednesday", "Thursday",
                 "Friday", "Saturday", "Sunday"]
df["weekday"] = dates.dt.dayofweek.map(dict(enumerate(weekday_names)))

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(OUTPUT, index=False)