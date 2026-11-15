from pathlib import Path
import pandas as pd

INPUT = Path("data/clean/events.csv")
OUTPUT = Path("data/transformed/events.csv")

df = pd.read_csv(
    INPUT,
    dtype={
        "user_id": "string",
        "timestamp": "string",
        "event_type": "string",
    },
)

df["date"] = df["timestamp"].str[:10]

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(OUTPUT, index=False)