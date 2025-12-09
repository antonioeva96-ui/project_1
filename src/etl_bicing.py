from pathlib import Path

import pandas as pd


RAW_FILES = [
    Path("data/raw/bicing_2018_08.csv"),
    Path("data/raw/bicing_2019_01.csv"),
]

CURATED_PATH = Path("data/curated/bicing_clean.parquet")


def load_and_concat(files):
    dfs = []
    for f in files:
        df = pd.read_csv(f)
        dfs.append(df)
    return pd.concat(dfs, ignore_index=True)


def run_etl():
    df = load_and_concat(RAW_FILES)

    # Rename id for clarity
    df = df.rename(columns={"id": "station_id"})

    # Convert datetime: e.g., "01/08/18 17:43:08"
    df["timestamp"] = pd.to_datetime(
        df["updateTime"], format="%d/%m/%y %H:%M:%S", errors="coerce"
    )

    # Drop rows without a valid timestamp
    df = df.dropna(subset=["timestamp"])

    # Cast to numeric types
    df["bikes"] = pd.to_numeric(df["bikes"], errors="coerce")
    df["slots"] = pd.to_numeric(df["slots"], errors="coerce")
    df["altitude"] = pd.to_numeric(df["altitude"], errors="coerce")

    # Remove rows with missing bike/slot counts
    df = df.dropna(subset=["bikes", "slots"])

    # Time features
    df["hour"] = df["timestamp"].dt.hour
    df["weekday"] = df["timestamp"].dt.weekday  # 0=Monday, 6=Sunday
    df["is_weekend"] = df["weekday"].isin([5, 6]).astype(int)

    # Flag empty station
    df["is_empty"] = (df["bikes"] == 0).astype(int)

    # Ensure curated folder exists
    CURATED_PATH.parent.mkdir(parents=True, exist_ok=True)

    # Save to Parquet
    df.to_parquet(CURATED_PATH, index=False)

    print(f"Final rows: {len(df)}")
    print(f"Saved to: {CURATED_PATH}")


if __name__ == "__main__":
    run_etl()
