from pathlib import Path

import pandas as pd

INPUT = Path("data/raw/events.csv")
OUTPUT = Path("data/clean/events.csv")

VALID_EVENT_TYPES = {"click", "login", "purchase", "scroll", "view"}

df = pd.read_csv(
    INPUT,
    dtype={
        "user_id": "string",
        "timestamp": "string",
        "event_type": "string",
    },
)

# Trim text fields and treat blank fields as missing.
for column in ("user_id", "timestamp", "event_type"):
    df[column] = df[column].str.strip()

df = df.replace(r"^\s*$", pd.NA, regex=True)

# Drop rows with any missing fields.
df = df.dropna()

# Keep only the valid, lowercase event types.
df = df[df["event_type"].isin(VALID_EVENT_TYPES)].copy()

# Keep only positive, whole-number durations.
duration = pd.to_numeric(df["duration_seconds"], errors="coerce")
valid_duration = duration.notna() & (duration > 0) & duration.mod(1).eq(0)
df = df.loc[valid_duration].copy()
duration = duration.loc[valid_duration]

# Parse the mixed timestamp formats without converting time zones.
timestamp = pd.to_datetime(
    df["timestamp"],
    format="mixed",
    errors="coerce",
)
valid_timestamp = timestamp.notna()

df = df.loc[valid_timestamp].copy()
duration = duration.loc[valid_timestamp]
timestamp = timestamp.loc[valid_timestamp]

# Write timestamps as YYYY-MM-DDTHH:MM:SS and durations as integers.
df["timestamp"] = timestamp.dt.strftime("%Y-%m-%dT%H:%M:%S")
df["duration_seconds"] = duration.astype("int64")

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(OUTPUT, index=False)
